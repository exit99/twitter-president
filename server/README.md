2. Symlink supervisor file

`cd /etc/nginx/sites-enabled && ln -s /srv/www/kazanski/server/nginx/kazanski.com`
`cp /srv/www/kazanski/server/gunicorn/kazanski.conf /etc/init/kazanski.conf`
