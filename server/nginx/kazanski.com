server {
    listen 80;
    server_name upcoachme.com;

     location / {
         include uwsgi_params;
         uwsgi_pass unix:/tmp/kazanski.sock;
     }

     location /static {
         alias /srv/www/kazanski/static;
     }
}
