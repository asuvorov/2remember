# Deployment

This provides Guideline on how to deploy and configure `Django/Python` Project from scratch under `Ubuntu Server` (`AWS` Instance), with `Nginx` and `uWSGI`.

---

## Amazon Web Services

### EC2 Instance

1. Sign-up / sign-in to **AWS Management Console** ([aws.amazon.com](http://aws.amazon.com)).

2. Create / launch **EC2 Instance**:
   
    2.1 *(optional)* Allocate **`ElasticIP`** and associate it with Instance.
   
    2.2 *(optional)* Configure **`Security Groups`**, i.e. open Ports (e.g. `SSH`, all `TCP`, all `UDP`, all `ICMP`, `HTTP`, `HTTPS`).
   
    2.3 Create **`SSH-Keypair`** and store it somewhere on your Computer (it's highly recommended to keep **SSH Keys** in **`$HOME/.ssh/`**).
   
   ```bash
   [~]$ ssh-keygen
   ```
   
    2.4 Change **`SSH-Keypair`** Access Rights:
   
   ```bash
   [~]$ sudo chmod 400 <PATH_TO_SSH-Keypair>
   ```
   
    2.5 *(optional)* Register (buy) Domain Name (e.g. **`example.com`**) at DNS Registrar (e.g. [goDaddy](http://godaddy.com) or [Name](http://name.com)) and associate [*.example.com](*.example.com) with **`ElasticIP`** (Type A).
   
    2.6 Connect to Instance via **SSH**, e.g.
   
   ```bash
   [~]$ ssh -i <PATH_TO_SSH-Keypair> ubuntu@52.24.65.219
   ```

---

## Setting up Ubuntu Instance (after connecting via SSH)

### Install Essentials

```bash
[~]$ sudo apt-get update && sudo apt-get upgrade
[~]$ sudo apt-get install -y build-essential curl g++ gcc gettext git make libc-dev libffi-dev memcached pkg-config wget
[~]$ sudo apt-get install -y apt-transport-https ca-certificates dirmngr software-properties-common
[~]$ sudo apt-get install -y python3-dev python3-pip python3-virtualenv default-libmysqlclient-dev python3-psycopg2
[~]$ sudo apt-get install -y nodejs npm
```

### Install MySQL Client/Server

1. Install **`MySQL`**:
   
   ```bash
   [~]$ sudo apt-get install -y mysql-server mysql-client
   ```

2. Configure **`MySQL`** *(optional)*. Not required for the **Staging / Production** Environments:
   **NOTE**: The default Password for the `root` User is `root`
   
   **NOTE**: Replace **`<DB_USERNAME>`** and **`<DB_PASSWORD>`** with the actual Username and Password you're going to use in your **`Django`** Project to connect to **MySQL**
   
   ```bash
   [~]$ sudo mysql -u root -p
   
        mysql> create user "<DB_USERNAME>"@"localhost" identified by "<DB_PASSWORD>";
        mysql> grant all privileges on * . * to "<DB_USERNAME>"@"localhost";
        mysql> exit
   ```

3. Create working Database *(optional)*. Not required for the **Staging / Production** Environments:
   
   ```bash
   [~]$ mysql -u <DB_USERNAME> -p
   
        mysql> create database <DB_NAME>;
        mysql> exit
   ```

### Install ElasticSearch Server

Installation and configuration of **`ElasticSearch`** originally taken from [How to Install Elasticsearch 8 on Ubuntu 24.04, 22.04, or 20.04 - LinuxCapable](https://linuxcapable.com/how-to-install-elasticsearch-8-on-ubuntu-linux/).

0. Install Java 8
   
   ```bash
   [~]$ sudo apt install default-jre && sudo apt install openjdk-8-jdkr
   ```

1. Download and install the Public Signing Key:
   
   ```bash
   [~]$ wget -q https://artifacts.elastic.co/GPG-KEY-elasticsearch -O- | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
   [~]$ echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
   [~]$ echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
   ```

2. Run `apt-get update` and the Repository is ready for Use:
   
   ```bash
   [~]$ sudo apt-get update && sudo apt-get install -y elasticsearch
   ```

3. Enable and start ElasticSearch:
   
   ```bash
   [~]$ sudo systemctl daemon-reload
   [~]$ sudo systemctl enable elasticsearch.service
   [~]$ sudo systemctl start  elasticsearch.service
   ```

4. Make sure service is running
   
   ```bash
   [~]$ curl http://localhost:9200
   ```

5. Other useful Commands
   
   ```bash
   [~]$ service elasticsearch status
   
   [~]$ sudo systemctl restart elasticsearch.service
   [~]$ sudo systemctl stop elasticsearch.service
   ```

6. Rebuild Indexes:
   
   ```bash
   [~]$ cd /opt/app/2remember/src
   [/opt/apps/2remember/src]$ python manage.py rebuild_index -v2
   ```

### Install Bower & LessJS

```bash
[~]$ sudo npm install -g bower less recess
```

---

## Setting up Django/Python Project (after connecting via SSH)

1. Cloning the Project:
   
    1.1 Creating working Directory:
   
   ```bash
   [~]$ sudo chown ubuntu:ubuntu /opt
   [~]$ mkdir /opt/apps
   ```
   
    1.2 Cloning Project:
   
   **NOTE**: If cloning via **SSH** Link - don't forget to add **SSH Key**, created via **`ssh-keygen`**, to the **Git** Account
   
   ```bash
   [~]$ cd /opt/apps
   [/opt/apps]$ git clone git@github.com:asuvorov/2remember.git
   
   or
   
   [/opt/apps]$ git clone https://github.com/asuvorov/2remember.git
   ```

2. Installing Virtual Environment and Project Dependencies:
   
   ```bash
   [/opt/apps]$ cd 2remember
   [/opt/apps/2remember]$ git checkout dev
   [/opt/apps/2remember]$ virtualenv .env
   [/opt/apps/2remember]$ . .env/bin/activate
   [/opt/apps/2remember]$ pip install --no-cache-dir -r requirements.txt
   ```

3. Export Environment Variables. For the **Staging** Environment add the following to the End of the **`~/.profile`** File:
   
   **NOTE**: An Example of the **`.profile`** File can be found at [2remember/deployment/.profile at feat/pre-release · asuvorov/2remember · GitHub](https://github.com/asuvorov/2remember/blob/feat/pre-release/deployment/.profile)
   
   ```bash
   [/opt/apps/2remember]$ cp /opt/apps/2remember/deployment/.profile ~
   [/opt/apps/2remember]$ source ~/.profile
   ```

4. Setting up the Project:
   
   ```bash
   [/opt/apps/2remember]$ cd src
   [/opt/apps/2remember/src]$ mkdir media logs
   [/opt/apps/2remember/src]$ python manage.py migrate
   [/opt/apps/2remember/src]$ python manage.py loaddata admin categories faq_sections faq site teams team_members
   [/opt/apps/2remember/src]$ python manage.py bower install
   [/opt/apps/2remember/src]$ python manage.py collectstatic --clear --no-input
   [/opt/apps/2remember/src]$ python manage.py createcachetable
   ```

5. Create an Admin Account to access Django Admin Panel:
   
   **NOTE:** Simply follow the Prompts
   
   ```bash
   [/opt/apps/2remember/src]$ python manage.py createsuperuser
   ```

6. Run the Server:
   
   ```bash
   [/opt/apps/2remember/src]$ python manage.py runserver
   ```

---

## Serving Django/Python with uWSGI/Nginx

Installation and configuration of uWSGI/Nginx originally taken from [here](http://posterous.adambard.com/start-to-finish-serving-mysql-backed-django-w).

https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#nginx-and-uwsgi-and-test-py

1. Generate private Key and SSL Certificate:
   
    1.1 Generate the private Key and CSR locally:
   
   ```bash
   [/opt/apps]$ openssl req -new -newkey rsa:2048 -nodes -keyout 2remember.key -out 2remember.csr
   ```
   
    1.2 Generate/buy the SSL Certificate from [name.com](https://www.name.com/)
   
    1.3 Create a new File for storing the **SSL Certificate**:
   
   ```bash
   [/opt/apps]$ touch 2remember.cer
   ```
   
    1.4 Copy/paste the generated SSL Certificate into the `/opt/apps/2remember.cer` File

2. Setting up **uWSGI** for the **Staging** Environment:
   
    2.1 Install **uWSGI**:
   
   ```bash
   [~]$ sudo apt-get install -y uwsgi uwsgi-plugin-python3
   ```
   
    2.2 Run daemonized **uWSGI**:
   
    2.2.1 Copy configuration File(s):
   
   ```bash
   [~]$ cp /opt/apps/2remember/deployment/opt/apps/uwsgi.ini /opt/apps/
   
   [~]$ sudo cp /opt/apps/2remember/deployment/etc/init/uwsgi.conf /etc/init/
   ```
   
    2.2.2 If **uWSGI** is located at **`/usr/local/bin`** (failed to run Service), create following Link:
   
   ```bash
   [~]$ sudo ln /usr/local/bin/uwsgi /usr/bin/uwsgi
   ```
   
    2.2.3 Run/reload/terminate daemonized **uWSGI**:
   
   ```bash
   [~]$ sudo uwsgi --ini    /opt/apps/uwsgi.ini --daemonize /var/log/uwsgi.log --pidfile /tmp/project-master.pid
   [~]$ sudo uwsgi --reload /tmp/project-master.pid
   [~]$ sudo uwsgi --stop   /tmp/project-master.pid
   ```

3. Setting up **Nginx** for the **Staging** Environment:
   
    3.1 Install **Nginx**:
   
   ```bash
   [~]$ sudo apt-get install -y nginx
   ```
   
    3.2 Configure **Nginx**:
   
    3.2.1 Create / update **uWSGI** Configuration File (usually, not needed):
   
   **NOTE**: An Example of the **`uwsgi_params`** File can be found at https://github.com/asuvorov/2remember/blob/feat/pre-release/deployment/etc/nginx/uwsgi_params
   
   ```bash
   [~]$ sudo nano /etc/nginx/uwsgi_params
   
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
   ```
   
    3.2.2 Create following Directories:
   
   ```bash
   [~]$ mkdir /opt/nginx
   [~]$ mkdir /opt/nginx/{sites-available,sites-enabled}
   ```
   
    3.2.3 Open the **Nginx** Configuration File for updating:
   
   ```bash
   [~]$ sudo nano /etc/nginx/nginx.conf
   ```
   
   and add the following Line within the **http** Section, right after the Line, that reads **`include/etc/nginx/conf.d/*.conf`**:
   
   ```bash
   include /opt/nginx/sites-enabled/*;
   ```
   
    3.3 Copy the actual Project Configuration File:
   
   ```bash
   [~]$ cp /opt/apps/2remember/deployment/opt/nginx/sites-available/2remember /opt/nginx/sites-available/
   ```
   
    3.4 Create the following Link:
   
   ```bash
   [~]$ ln -s /opt/nginx/sites-available/2remember /opt/nginx/sites-enabled/2remember
   ```
   
    3.5 Restart **Nginx**:
   
   ```bash
   [~]$ sudo /etc/init.d/nginx restart
   ```

---

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

---

## Setting up Supervisor

Installation and Configuration originally taken from [here](http://supervisord.org/).
