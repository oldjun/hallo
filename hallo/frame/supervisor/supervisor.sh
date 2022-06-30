#!/bin/bash

mkdir -p log
export FLASK_APP_CONFIG='production'
supervisord -c /etc/supervisord.conf
