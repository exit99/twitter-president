#!/usr/bin/env bash

# update packages
apt-get update
apt-get upgrade

# redis
apt-get install -y python-software-properties
add-apt-repository -y ppa:chris-lea/redis-server
apt-get update
apt-get install -y redis-server

# setup redis
sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis/redis.conf
/etc/init.d/redis-server restart

# mysql
apt-get install -y mysql-client
DEBIAN_FRONTEND=noninteractive apt-get install -y -q mysql-server

# setup mysql
sed -i 's/bind-address\t\t= 127.0.0.1/bind-address\t\t= 0.0.0.0/g' /etc/mysql/my.cnf
sed -i 's/\[mysqld\]/\[mysqld\]\ncharacter-set-server=utf8\ncollation-server=utf8_general_ci\n/g' /etc/mysql/my.cnf
/etc/init.d/mysql restart
mysql --user root --execute='CREATE DATABASE election_2016;'
mysql --user root --execute='CREATE DATABASE test_election_2016;'
mysql --user root --execute='CREATE USER "test"@"%";'
mysql --user root --execute='CREATE USER "election"@"%";'
mysql --user root --execute='GRANT ALL ON *.* TO "test"@"%";'
mysql --user root --execute='GRANT ALL ON *.* TO "election"@"%";'
