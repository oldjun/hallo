#!/bin/bash

project=%(project)s
base_path=%(base_path)s
echo $base_path

if [ ! -d $base_path/supervisor ];then
    mkdir $base_path/supervisor
fi

supervisord_conf=$base_path/supervisor/supervisord.conf
echo $supervisord_conf

if [ ! -d $base_path/log ];then
    mkdir $base_path/log
fi

python3 -m venv $base_path/venv
source $base_path/venv/bin/activate
pip3 install -r $base_path/requirements.txt
pip3 install uwsgi
pip3 install supervisor
echo_supervisord_conf > $supervisord_conf
sed -i "s#/tmp/supervisor.sock#$base_path/log/supervisor.sock#g" $supervisord_conf
sed -i "s#/tmp/supervisord.log#$base_path/log/supervisor.log#g" $supervisord_conf
sed -i "s#/tmp/supervisord.pid#$base_path/log/supervisord.pid#g" $supervisord_conf
sed -i "s#\;\[include\]#\[include\]#g" $supervisord_conf
sed -i "s#\;files = relative/directory#files = $base_path/supervisor/conf.d#g" $supervisord_conf

if [ ! -d $base_path/supervisor/conf.d ];then
    mkdir -p $base_path/supervisor/conf.d
else
    if [ ! -f $base_path/supervisor/conf.d/uwsgi.ini ];then
        touch $base_path/supervisor/conf.d/uwsgi.ini
    fi
fi
cat > $base_path/supervisor/conf.d/uwsgi.ini << EOF
[program:$project]
command = uwsgi --ini uwsgi.ini
directory = $base_path
autostart = true
autorestart = true
redirect_stderr = true
stopasgroup = true
EOF

if [ ! -f $base_path/uwsgi.ini ];then
    touch $base_path/uwsgi.ini
fi
cat > $base_path/uwsgi.ini << EOF
[uwsgi]
http = :8080
;socket = log/uwsgi.sock
;chmod-socket = 664
hook-master-start = unix_signal:15 gracefully_kill_them_all
need-app = true
die-on-term = true
show-config = true
callable = app
wsgi-file = main.py
enable-threads = true
threads = 8
disable-logging = true
logto = log/uwsgi.log
ignore-sigpipe
ignore-write-errors
disable-write-exception
EOF

num=`ps -ef|grep $base_path/venv/bin/supervisord|grep -v grep|wc -l`
if [ $num -gt 0 ];then
    supervisorctl -c $supervisord_conf stop all
    supervisorctl -c $supervisord_conf shutdown
fi
supervisord -c $supervisord_conf

status_shell=$base_path/supervisor/status.sh
rm -rf $status_shell
touch $status_shell
chmod a+x $status_shell
cat > $status_shell << EOF
#!/bin/bash

source $base_path/venv/bin/activate
supervisorctl -c $supervisord_conf status
EOF

start_shell=$base_path/supervisor/start.sh
rm -rf $start_shell
touch $start_shell
chmod a+x $start_shell
cat > $start_shell << EOF
#!/bin/bash

source $base_path/venv/bin/activate
num=\`ps -ef|grep $base_path/venv/bin/supervisord|grep -v grep|wc -l\`
if [ \$num -eq 0 ];then
    supervisord -c $supervisord_conf
else
    supervisorctl -c $supervisord_conf start $project
fi
EOF

stop_shell=$base_path/supervisor/stop.sh
rm -rf $stop_shell
touch $stop_shell
chmod a+x $stop_shell
cat > $stop_shell << EOF
#!/bin/bash

source $base_path/venv/bin/activate
supervisorctl -c $supervisord_conf stop $project
EOF

restart_shell=$base_path/supervisor/restart.sh
rm -rf $restart_shell
touch $restart_shell
chmod a+x $restart_shell
cat > $restart_shell << EOF
#!/bin/bash

source $base_path/venv/bin/activate
supervisorctl -c $supervisord_conf restart $project
EOF

shutdown_shell=$base_path/supervisor/shutdown.sh
rm -rf $shutdown_shell
touch $shutdown_shell
chmod a+x $shutdown_shell
cat > $shutdown_shell << EOF
#!/bin/bash

source $base_path/venv/bin/activate
supervisorctl -c $supervisord_conf stop all
supervisorctl -c $supervisord_conf shutdown
EOF