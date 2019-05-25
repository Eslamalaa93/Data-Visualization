#!/bin/bash
#### This script is for deploying VisualizationBackend and setup its environment

read -p "Enter uid: " uid
read -p "Enter database dumb file name: " dumbFileName
read -p "Enter server IP: " serverName

# install python 3.6
echo "................Start installing python................"
sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get update -y
sudo apt-get install -y python3.6
sudo apt-get install -y python3-pip
echo "................End installing python................"

# install mysql-server
echo "................Start installing mysql-server................"
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password admin'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password admin'
sudo apt install -y mysql-server mysql-client
sudo apt-get install -y libmysqlclient-dev
echo "[mysqld]" >> /etc/mysql/my.cnf
echo "sql_mode = \"STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION\"" >> /etc/mysql/my.cnf
sudo service mysql restart
echo "................End installing mysql-server................"

# install virtualenv and virtualenvwrapper
echo "................Start installing virtualenvwrapper................"
sudo pip3 install virtualenv virtualenvwrapper
echo "................End installing virtualenvwrapper................"

# install git
echo "................Start installing git................"
sudo apt-get install -y git
echo "................End installing git................"

# install unrar and unzip
echo "................Start installing unzip and unrar................"
sudo apt-get install -y unrar
sudo apt-get install -y unzip
echo "................End installing unzip and unrar................"

# clone project repo to home dir
echo "................Start cloning project................"
cd ~
git clone https://pro_mining:123456@olc.orange-labs.fr/gitblit/git/OBS-ProcessMining/visualization-backend.git

# configure VirtualEnvWrapper
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/Env
source /usr/local/bin/virtualenvwrapper.sh
echo "................End cloning project................"

# create virtualenv and install project requirements
echo "................Start creating virtualenv and installing project requirements................"
mkvirtualenv visualization-backend
cd ~/visualization-backend/
pip install -r requirements.txt
echo "................End creating virtualenv and installing project requirements................"

# collect project static files to /static dir
echo "................Start collecting project static files to /static dir................"
python3 manage.py collectstatic
echo "................End collecting project static files to /static dir................"

echo "................Start migrating database and importing dumb................"
# create database
echo CREATE SCHEMA dlt_weekly | mysql --host=localhost --user=root --password=admin

# migrate database
cd ~/visualization-backend/
python3 manage.py migrate

# import database dumb
cd ~/visualization-backend/DatabaseDumbs/
sudo unzip $dumbFileName.zip -d .
cd $dumbFileName
cat *.sql | mysql --host=localhost --user=root --password=admin dlt_weekly
echo "................End migrating database and importing dumb................"

echo "................Start installing and configuring uWSGI................"
# Allow port 8080
sudo ufw allow 8080

# installing uWSGI
sudo apt-get install -y python3-dev
sudo pip3 install uwsgi

# configure uWSGI
sudo mkdir -p /etc/uwsgi/sites
cd /etc/uwsgi/sites

# create uWSGI configuration file
sudo touch VisualizationBackend.ini
sudo cat > VisualizationBackend.ini <<EOL
[uwsgi]
project = visualization-backend
uid = $uid
base = /home/%(uid)

chdir = %(base)/%(project)
home = %(base)/Env/%(project)
module = VisualizationBackend.wsgi:application

master = true
processes = 5

socket = /run/uwsgi/VisualizationBackend.sock
chown-socket = %(uid):www-data
chmod-socket = 660
vacuum = true

req-logger = file:/tmp/reqlog
logger = file:/tmp/errlog
EOL

#Create a systemd Unit File for uWSGI
sudo touch /etc/systemd/system/uwsgi.service
sudo cat > /etc/systemd/system/uwsgi.service <<EOL
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown $uid:www-data /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOL
echo "................End installing and configuring uWSGI................"

echo "................Start installing and configuring Nginx................"
# Install and Configure Nginx
sudo apt-get install -y nginx

sudo touch /etc/nginx/sites-available/VisualizationBackend
sudo cat > /etc/nginx/sites-available/VisualizationBackend <<EOL
server {
    listen 8080;
    server_name $serverName;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/$uid/visualization-backend;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/run/uwsgi/VisualizationBackend.sock;
    }
}
EOL

sudo ln -s /etc/nginx/sites-available/VisualizationBackend /etc/nginx/sites-enabled

sudo systemctl restart nginx

sudo systemctl start uwsgi

sudo ufw delete allow 8080
sudo ufw allow 'Nginx Full'

sudo systemctl enable nginx
sudo systemctl enable uwsgi

echo "................End installing and configuring Nginx................"








