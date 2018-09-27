# Lit Bit - Auto Generated Poems
LitBit generates a small poem from lines popular literature.

### Tech
* Python 2.7
* Flask
* Uwsgi

### Dev Environment Setup
1. Clone repo
1. `apt-get install python-dev python-pip`
1. `pip install virtualenv`
1. `virtualenv env`
1. `source env/bin/activate`
1. `pip install uwsgi flask hashids`
1. `flask run`

## UWSGI and Nginx Setup (Ubuntu 16.04 / systemd service)
1. Copy `litbit.ini.example` to `litbit.ini` and edit the paths
1. Create nginx site conf:
  ```nginx
  server {
    listen 80;
    server_name litbit.test;
    
    location / {
      include uwsgi_params;
      uwsgi_pass unix:///var/www/litbit/app.sock 
      # replace above sock with your app sock file path, must have leading unix:// before path
    }
  }
  ```
1. Add domain name to `/etc/hosts`
1. Copy `litbit.service.example` to `/etc/systemd/system/litbit.service` and edit paths
1. `sudo systemctl enable litbit`
1. `sudo service litbit restart` and `sudo service nginx restart`
1. Error logs can be found at:
  * `journal ctl -u litbit.service`
  * nginx error logs
  * `logs/app.log`

### Useful links:
* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
* https://code.luasoftware.com/tutorials/nginx/setup-nginx-and-uwsgi-for-flask-on-ubuntu/

### Adding books
1. Grab free use books from Project Gutenberg or similar source in .txt format. 
1. Remove all unnecessary text from before or after the book text (ex: table of contents, prefaces, etc)
1. Add the .txt file to the books/ directory
1. Grab a cover image, as well as title, author, and year details.
1. Run the `flask register` command to add new books to the books.json list
