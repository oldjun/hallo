create table if not exists `user` (
    `id` int unsigned not null auto_increment,
    `username` varchar(32) not null default '',
    `phone` varchar(16) not null default '',
    `money` decimal(10,2) not null default 0,
    `gender` tinyint unsigned not null default 0,
    `password` varchar(128) not null default '',
    `time` timestamp not null default current_timestamp,
    primary key(`id`),
    unique key `idx_username` (`username`),
    key `idx_phone` (`phone`),
    key `idx_time` (`time`)
) engine=InnoDB default charset=utf8mb4;