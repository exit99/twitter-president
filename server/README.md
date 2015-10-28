2. Symlink supervisor file

`cd /etc/nginx/sites-enabled && ln -s /srv/www/kazanski/server/nginx/kazanski.com`
`cp /srv/www/kazanski/server/gunicorn/kazanski.conf /etc/init/kazanski.conf`


## For deployment

do the above
pip install reqs

install bower components
restart gunicorn
restrart ngninx



DONT commit the bower_component files.

## Server requirements

All the python devel stuff
node
git
mysql
redis
bower
npm
coffeesript
less

