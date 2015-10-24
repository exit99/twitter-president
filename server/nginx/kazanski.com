server {
    server_tokens off;
    server_name kazanski.com www.kazanski.com;

     location / {
         include uwsgi_params;
         uwsgi_pass unix:/tmp/kazanski.sock;
     }

     location /static {
         alias /srv/www/kazanski/static;
     }
}
