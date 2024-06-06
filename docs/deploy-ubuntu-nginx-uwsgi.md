Deployment
==========
This provides Guideline on how to deploy and configure Django/Python Project from scratch under Ubuntu Server (AWS Instance), with Nginx and uWSGI.

-------------------
Amazon Web Services
-------------------
### EC2 Instance

1. Sign-up / sign-in to **AWS Management Console** ([aws.amazon.com](http://aws.amazon.com)).

2. Create / launch **EC2 Instance**:

    2.1 *(optional)* Allocate **`ElasticIP`** and associate it with instance.

    2.2 *(optional)* Configure **`Security Groups`**, i.e. open ports (e.g. SSH, all TCP, all UDP, all ICMP, HTTP, HTTPS).

    2.3 Create **`SSH-Keypair`** and store it somewhere on Computer (it's highly recommended to keep **SSH Keys** in **`$HOME/.ssh/`**).

    2.4 Change **`SSH-Keypair`** Access Rights:

            [~]# sudo chmod 400 <PATH_TO_SSH-Keypair>

    2.5 *(optional)* Register (buy) Domain Name (e.g. **`example.com`**) at DNS Registrar (e.g. [goDaddy](http://godaddy.com) or [Name](http://name.com)) and associate [*.example.com](*.example.com) with **`ElasticIP`** (Type A).

    2.6 Connect to Instance via **SSH**, e.g.

            [~]# ssh -i <PATH_TO_SSH-Keypair> ubuntu@52.24.65.219

-----------------------------------------------------
Setting up Ubuntu Instance (after connecting via SSH)
-----------------------------------------------------
### Presets

            [~]# sudo apt-get update
            [~]# sudo apt-get upgrade

            [~]# sudo apt-get install wget gcc make g++ unzip python-setuptools python-pip python-dev memcached
            [~]# sudo apt-get install libcurl4-openssl-dev libxml2-dev libxslt1-dev

            [~]# sudo easy_install -U pip
            [~]# sudo easy_install virtualenv

### Papertrail centralized logging *(optional)*

Just follow [this](http://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-python-apps/) Directions.

### MySQL

1. Install MySQL:

            [~]# sudo apt-get install mysql-server mysql-client libmysqlclient-dev

2. Configure MySQL *(optional)*. Not required for the **Staging / Production** Environments:

            [~]# mysql -u root -p

            mysql> create user "USERNAME"@"localhost" identified by "PASSWORD";
            mysql> grant all privileges on * . * to "USERNAME"@"localhost";
            mysql> ^D

3. Create working Database *(optional)*. Not required for the **Staging / Production** Environments:

            [~]# mysql -u USERNAME -p

            mysql> create database DBNAME;
            mysql> ^D

### Installing / upgrading git:

            [~]# sudo apt-get install git

### Installing Dependencies for PIL (Python image libraries):

1. Mandatory:

            [~]# sudo apt-get install libjpeg-dev libjpeg-dev zlib1g-dev libpng12-dev libfreetype6-dev
            [~]# sudo apt-get install build-dep python-imaging
            [~]# sudo ln -s /usr/include/freetype2 /usr/local/include/freetype
            [~]# sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
            [~]# sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
            [~]# sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

2. Optional (if PIL was installed before libjpeg*):

            [~]# sudo pip install -I pillow

### Bower

1. Installing Dependecies:

            [~]# sudo apt-get install nodejs nodejs-legacy npm

2. Installing Bower

            [~]# sudo chown -R ubuntu:ubuntu /home/ubuntu
            [~]# sudo chown -R $USER /usr/local
            [~]# sudo npm install -g bower

--------------------------------
Setting up Django/Python Project
--------------------------------

1. Cloning the Project:

    1.1 Creating working Directory:

            [~]# sudo chown ubuntu:ubuntu /opt
            [~]# mkdir /opt/apps

    1.2 Cloning Project (don't forget to add **SSH Key**, created via **`ssh-keygen`**, to Git Account):

            [~]# cd /opt/apps
            [/opt/apps]# git clone git@github.com:asuvorov/saneside.git

2. Installing Virtual Environment and Project Dependencies:

            [/opt/apps]# cd saneside
            [/opt/apps/saneside]# virtualenv ve --no-site-packages
            [/opt/apps/saneside]# . ve/bin/activate
            [/opt/apps/saneside]# pip install --no-cache-dir -r requirements.txt

3. Export Environment Variables. For the **Staging** Environment add the following to the End of the `/home/ubuntu/.bashrc` File:

            # Custom Environment Variables
            export ENVIRONMENT=staging
            export DJANGO_SETTINGS_MODULE=settings.staging
            export AWS_SANESIDE_STAGING_DB_NAME=oyyyo_production
            export AWS_SANESIDE_STAGING_DB_USER=oyyyo_admin
            export AWS_SANESIDE_STAGING_DB_PASSWORD=Majestic12
            export AWS_SANESIDE_STAGING_DB_HOST=oyyyo.csisnutyjpxo.us-west-2.rds.amazonaws.com
            export AWS_SANESIDE_STAGING_DB_PORT=3306
            export AWS_SANESIDE_ACCESS_KEY_ID=AKIAJDPKYAFU34PQUOVA
            export AWS_SANESIDE_SECRET_ACCESS_KEY=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
            export AWS_SANESIDE_STAGING_BUCKET_NAME=saneside-media

4. Setting up Project:

            [/opt/apps/saneside/src]# python manage.py migrate
            [/opt/apps/saneside/src]# python manage.py bower install
            [/opt/apps/saneside/src]# python manage.py collectstatic
            [/opt/apps/saneside/src]# python manage.py runserver

---------------------------------
Setting up Django Cache Framework
---------------------------------

1. Create the Cache Table for the **Staging** and **Production** Environment:

            [/opt/apps/saneside/src]# python manage.py createcachetable

---------------------
Setting up Django SEO
---------------------

1. Create and run Migrations:

            [/opt/apps/saneside/src]# python manage.py makemigrations djangoseo
            [/opt/apps/saneside/src]# python manage.py migrate djangoseo --fake-initial

2. Go into Django Admin Section `/admin/sites/site/1/` and change the Domain Name to "www.saneside.com".

--------------------------------------
Serving Django/Python with uWSGI/Nginx
--------------------------------------
Installation and configuration of uWSGI/Nginx originally taken from [here](http://posterous.adambard.com/start-to-finish-serving-mysql-backed-django-w).

https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#nginx-and-uwsgi-and-test-py

1. Generate private Key and SSL Certificate:

    1.1 Generate the private Key and CSR locally:

            [/opt/apps]# openssl req -new -newkey rsa:2048 -nodes -keyout 2remember.key -out 2remember.csr

    1.2 Generate/buy the SSL Certificate from [name.com](https://www.name.com/)

    1.3 Create a new File for storing the **SSL Certificate**:

            [/opt/apps]# touch 2remember.cer

    1.4 Copy/paste the generated SSL Certificate into the `/opt/apps/2remember.cer` File

2. Setting up **uWSGI** for the **Staging** Environment:

    2.1 Install **uWSGI**:

            [~]# sudo apt-get install uwsgi
            [~]# sudo apt-get install uwsgi-plugin-python3

    2.2 Run daemonized **uWSGI**:

    2.2.1 Copy configuration File:

            [~]# sudo cp /opt/apps/saneside/deployment/staging/uwsgi/etc/init/uwsgi.conf /etc/init/

    2.2.2 If **uWSGI** is located at **`/usr/local/bin`** (failed to run Service), create following Link:

            [~]# sudo ln /usr/local/bin/uwsgi /usr/bin/uwsgi

    2.2.3 Run/terminate daemonized **uWSGI**:

            [~]# sudo start uwsgi
            [~]# sudo stop uwsgi

3. Setting up **Nginx** for the **Staging** Environment:

    3.1 Install **Nginx**:

            [~]# sudo apt-get install nginx

    3.2 Configure **Nginx**:

    3.2.1 Create / update configuration File (usually, not needed):

            [~]# sudo nano /etc/nginx/uwsgi_params

            # /etc/nginx/uwsgi_params

            uwsgi_param  QUERY_STRING       $query_string;
            uwsgi_param  REQUEST_METHOD     $request_method;
            uwsgi_param  CONTENT_TYPE       $content_type;
            uwsgi_param  CONTENT_LENGTH     $content_length;

            uwsgi_param  REQUEST_URI        $request_uri;
            uwsgi_param  PATH_INFO          $document_uri;
            uwsgi_param  DOCUMENT_ROOT      $document_root;
            uwsgi_param  SERVER_PROTOCOL    $server_protocol;

            uwsgi_param  REMOTE_ADDR        $remote_addr;
            uwsgi_param  REMOTE_PORT        $remote_port;
            uwsgi_param  SERVER_PORT        $server_port;
            uwsgi_param  SERVER_NAME        $server_name;

    3.2.2 Create following Directories:

            [~]# mkdir /opt/nginx
            [~]# mkdir /opt/nginx/{sites-available,sites-enabled}

    3.2.3 Add the following Line within the **http** section of **`/etc/nginx/nginx.conf`**, right after the line that reads **`include/etc/nginx/conf.d/*.conf`**:

            include /opt/nginx/sites-enabled/*;

    3.3 Copy configuration File:

            [~]# sudo cp /opt/apps/2remember/deployment/staging/nginx/sites-available/2remember /opt/nginx/sites-available/

    3.4 Create following Link:

            [~]# ln -s /opt/nginx/sites-available/2remember /opt/nginx/sites-enabled/2remember

    3.5 Restart **Nginx**:

            [~]# sudo /etc/init.d/nginx restart

-------------
ElasticSearch
-------------
Installation and configuration of ElasticSearch originally taken from [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-repositories.html).

0. Install Java 8

            [~]# sudo apt-get install -y python-software-properties
            [~]# sudo add-apt-repository -y ppa:webupd8team/java
            [~]# sudo apt-get update && sudo apt-get install -y oracle-java8-installer

1. Download and install the Public Signing Key:

            [~]# sudo wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
            [~]# sudo echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list

2. Run apt-get update and the repository is ready for use:

            [~]# sudo apt-get update && sudo apt-get install -y elasticsearch

3. Start ElasticSearch:

            [~]# sudo service elasticsearch start

4. Make sure service is running

            [~]# curl http://localhost:9200

5. Rebuild Indexes:

            [~]# cd /opt/app/saneside/src
            [/opt/apps/saneside/src]# python manage.py rebuild_index -v2

-----------------
Django Compressor
-----------------

1. Installing Dependecies:

            [~]# sudo apt-get install nodejs nodejs-legacy npm

            [~]# sudo npm cache clear
            [~]# sudo npm update npm -g
            [~]# sudo npm config set registry http://registry.npmjs.org/

2. Install "lessc" (and "recess", optional):

            [~]# sudo npm install -g less recess

3. Create Link:

            [~]# sudo ln -s /opt/apps/2remember/src/static/img/ /opt/apps/2remember/src/staticserve/CACHE/img/

---------------------
Setting up Supervisor
---------------------

Installation and Configuration originally taken from [here](http://supervisord.org/).
