#!/bin/bash

echo "========================================================================"
echo "=== Setting up Ubuntu Instance                                       ==="
echo "========================================================================"

echo ">>> INFO    : Install Essentials"
echo

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y build-essential curl g++ gcc gettext git make libc-dev libffi-dev memcached pkg-config wget
sudo apt-get install -y apt-transport-https ca-certificates dirmngr software-properties-common
sudo apt-get install -y python3-dev python3-pip python3-virtualenv default-libmysqlclient-dev python3-psycopg2
sudo apt-get install -y nodejs npm

echo ">>> INFO    : Install Bower & LessJS"
echo

sudo npm install -g bower less recess



echo "========================================================================"
echo "=== Setting up Django/Python Project                                 ==="
echo "========================================================================"

sudo chown ubuntu:ubuntu /opt

mkdir /opt/apps
cd    /opt/apps

git clone git@github.com:asuvorov/2remember.git

cd 2remember
git checkout dev
virtualenv .env && . .env/bin/activate
pip install --no-cache-dir -r requirements.txt

cp /opt/apps/2remember/deployment/.profile ~
source ~/.profile

cd src
mkdir media logs
python manage.py migrate
python manage.py loaddata admin categories faq_sections faq site teams team_members
python manage.py bower install
python manage.py collectstatic --clear --no-input
python manage.py createcachetable



echo "========================================================================"
echo "=== Setting up Infrastructure                                        ==="
echo "========================================================================"

echo ">>> INFO    : Install MySQL Client/Server"
echo

cd /opt/apps/2remember
sudo apt-get install -y mysql-server mysql-client
sudo mysql < ./docker_config/init_db.sq

echo ">>> INFO    : Install ElasticSearch Server"
echo

echo ">>> INFO    : Install AWS CLI"
echo

sudo snap install aws-cli --classic


echo "========================================================================"
echo "=== Serving Django/Python with uWSGI/Nginx                           ==="
echo "========================================================================"

echo ">>> INFO    : Generate private Key and SSL Certificate"
echo

echo ">>> INFO    : Setting up uWSGI"
echo

sudo apt-get install -y uwsgi uwsgi-plugin-python3
cp /opt/apps/2remember/deployment/opt/apps/uwsgi.ini /opt/apps/
sudo cp /opt/apps/2remember/deployment/etc/init/uwsgi.conf /etc/init/
sudo ln /usr/local/bin/uwsgi /usr/bin/uwsgi

sudo uwsgi --ini    /opt/apps/uwsgi.ini --daemonize /var/log/uwsgi.log --pidfile /tmp/project-master.pid

echo ">>> INFO    : Setting up Nginx"
echo

sudo apt-get install -y nginx
sudo cp /opt/apps/2remember/deployment/etc/nginx/uwsgi_params /etc/nginx
sudo cp /opt/apps/2remember/deployment/etc/nginx/nginx.conf   /etc/nginx

mkdir /opt/nginx
mkdir /opt/nginx/{sites-available,sites-enabled}
cp /opt/apps/2remember/deployment/opt/nginx/sites-available/2remember /opt/nginx/sites-available/
ln -s /opt/nginx/sites-available/2remember /opt/nginx/sites-enabled/2remember

sudo /etc/init.d/nginx restart



echo "========================================================================"
echo "=== Setting up Supervisor                                            ==="
echo "========================================================================"
