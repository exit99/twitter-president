server {
    listen 80;
    server_name upcoachme.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/srv/www/kazanski/kazanski.sock;
    }

    location /static {
        alias /srv/www/kazanski/static;
    }
}
~
