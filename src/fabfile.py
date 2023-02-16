# -----------------------------------------------------------------------------
# --- Deploy on Production
#
#     fab --hosts=52.24.65.219   --set=environment=production <deploy | update | restart>
#
# --- Deploy on Staging
#
#     fab --hosts=54.200.235.210 --set=environment=staging    <deploy | update | restart>
#
# -----------------------------------------------------------------------------
import time

from fabric.api import *
from fabric.colors import *
from fabric.contrib import django
from fabric.contrib.console import confirm

from progress.bar import Bar
from progress.spinner import Spinner


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ---
# --- INITIAL VARIABLES
# ---
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Hosts (all)
# env.hosts = [
#     "52.24.65.219",     # Production
#     "54.200.235.210",   # Staging
# ]
env.user = "ubuntu"
env.key_filename = "~/.ssh/UbuntuHome.pem"

# -----------------------------------------------------------------------------
# --- Git
env.branch = {
    "production":   "master",
    "staging":      "staging",
}

# -----------------------------------------------------------------------------
# --- App
env.app_name = "saneside"
env.app_repo = "git@github.com:asuvorov/{app_name}.git".format(app_name=env.app_name)
env.app_parent = "/opt/apps"
env.app_folder = "{app_parent}/{app_name}".format(
    app_parent=env.app_parent,
    app_name=env.app_name)
env.ve_activate = "source {app_folder}/ve/bin/activate".format(app_folder=env.app_folder)

# -----------------------------------------------------------------------------
# --- Environment
# env.environment = "staging"

env.variables = {
    "production": {
        "ENVIRONMENT":                          "production",
        "DJANGO_SETTINGS_MODULE":               "settings.production",
        "AWS_SANESIDE_PRODUCTION_DB_NAME":      "oyyyo_production",
        "AWS_SANESIDE_PRODUCTION_DB_USER":      "oyyyo_admin",
        "AWS_SANESIDE_PRODUCTION_DB_PASSWORD":  "Majestic12",
        "AWS_SANESIDE_PRODUCTION_DB_HOST":      "oyyyo.csisnutyjpxo.us-west-2.rds.amazonaws.com",
        "AWS_SANESIDE_PRODUCTION_DB_PORT":      "3306",
        "AWS_SANESIDE_ACCESS_KEY_ID":           "AKIAJDPKYAFU34PQUOVA",
        "AWS_SANESIDE_SECRET_ACCESS_KEY":       "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",
        "AWS_SANESIDE_PRODUCTION_BUCKET_NAME":  "saneside-media",
    },
    "staging": {
        "ENVIRONMENT":                          "staging",
        "DJANGO_SETTINGS_MODULE":               "settings.staging",
        "AWS_SANESIDE_STAGING_DB_NAME":         "saneside_staging",
        "AWS_SANESIDE_STAGING_DB_USER":         "root",
        "AWS_SANESIDE_STAGING_DB_PASSWORD":     "root",
        "AWS_SANESIDE_STAGING_DB_HOST":         "localhost",
        "AWS_SANESIDE_STAGING_DB_PORT":         "3306",
        "AWS_SANESIDE_ACCESS_KEY_ID":           "AKIAJDPKYAFU34PQUOVA",
        "AWS_SANESIDE_SECRET_ACCESS_KEY":       "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",
        "AWS_SANESIDE_STAGING_BUCKET_NAME":     "saneside-media",
    }
}

env.requirements_file = "requirements/{environment}.txt".format(environment=env.environment)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ---
# --- HELPERS
# ---
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def _spinner_sleep(delay=1, step=0.1):
    """Shows Spinner for `delay` in Seconds."""
    spinner = Spinner("Loading ")

    passed = 0
    while passed <= float(delay):
        time.sleep(step)

        passed += step

        spinner.next()

    spinner.finish()

    print "\n"


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ---
# --- TASKS
# ---
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def apt_upgrade():
    """Upgrade installed Packages."""
    print green("***" * 27)
    print green("*** Going to update & upgrade installed Packages...")

    with settings(warn_only=True):
        sudo("apt-get update  -y")
        sudo("apt-get upgrade -y")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def apt_install():
    """Install system Dependencies."""
    print green("***" * 27)
    print green("*** Going to install system Dependencies...")

    # -------------------------------------------------------------------------
    # --- Install system Dependencies
    print cyan("[---  INFO   ---] Install system Dependencies...")

    sudo("apt-get install -y wget gcc make g++ unzip memcached")
    sudo("apt-get install -y python-setuptools python-pip python-dev")
    sudo("apt-get install -y libcurl4-openssl-dev libxml2-dev libxslt1-dev")

    # -------------------------------------------------------------------------
    # --- Install PIP & VirtualEnv
    print cyan("[---  INFO   ---] Install PIP & Virtual Environment...")

    sudo("easy_install -U pip")
    sudo("easy_install virtualenv")

    # -------------------------------------------------------------------------
    # --- Install Git
    print cyan("[---  INFO   ---] Install Git...")

    sudo("apt-get install -y git")

    # -------------------------------------------------------------------------
    # --- Install PIL
    print cyan("[---  INFO   ---] Install PIL Dependencies...")

    sudo("apt-get install -y libjpeg-dev libjpeg-dev")
    sudo("apt-get install -y zlib1g-dev libpng12-dev libfreetype6-dev")

    sudo("apt-get build-dep -y python-imaging")

    with settings(warn_only=True):
        sudo("ln -s /usr/include/freetype2 /usr/local/include/freetype")
        sudo("ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib")
        sudo("ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib")
        sudo("ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def apt_install_mysql():
    """Install MySQL."""
    print green("***" * 27)
    print green("*** Going to install MySQL...")

    print yellow("[--- WARNING ---] Skip this Step...")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def npm_upgrade():
    """Upgrade NPM Packages."""
    print green("***" * 27)
    print green("*** Going to upgrade NPM Packages...")

    with settings(warn_only=True):
        sudo("npm update -g")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def npm_install():
    """Install NPM Packages."""
    print green("***" * 27)
    print green("*** Going to install NPM Packages...")

    # -------------------------------------------------------------------------
    # --- Install NodeJS & NPM
    print cyan("[---  INFO   ---] Install NodeJS & NPM...")

    sudo("apt-get install -y nodejs nodejs-legacy npm")

    sudo("npm cache clear")
    sudo("npm update npm -g")
    sudo("npm config set registry http://registry.npmjs.org/")

    # -------------------------------------------------------------------------
    # --- Install Bower
    print cyan("[---  INFO   ---] Install Bower...")

    sudo("chown -R {user}:{group} /home/{home}".format(
        user=env.user,
        group=env.user,
        home=env.user,
        ))
    sudo("chown -R $USER /usr/local")
    sudo("npm install -g bower")

    # -------------------------------------------------------------------------
    # --- Install Less CSS
    print cyan("[---  INFO   ---] Install Less CSS...")

    sudo("npm install -g less recess")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_wd_create():
    """Create working Directory."""
    print green("***" * 27)
    print green("*** Going to create working Directory...")

    sudo("chown -R {user}:{group} /opt".format(
        user=env.user,
        group=env.user,
        ))

    with settings(warn_only=True):
        run("mkdir {app_parent}".format(
            app_parent=env.app_parent,
            ))

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_git_clone():
    """Clone Django App."""
    print green("***" * 27)
    print green("*** Going to clone the Project...")

    with cd("{app_parent}".format(
            app_parent=env.app_parent,
            )):
        with settings(warn_only=True):
            run("rm -rf {app_folder}".format(
                app_folder=env.app_folder,
                ))

            run("git clone {app_repo}".format(
                app_repo=env.app_repo,
                ))

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_git_pull():
    """Pull Django App."""
    print green("***" * 27)
    print green("*** Going to Git pull the Project...")

    with cd("{app_folder}".format(
            app_folder=env.app_folder,
            )):
        # --- Pull the `master` Branch
        run("git checkout master")
        run("git pull")

        # --- Pull the working Branch
        run("git checkout {branch}".format(
            branch=env.branch[env.environment],
            ))
        run("git pull origin {branch}".format(
            branch=env.branch[env.environment],
            ))

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_ve_install():
    """Set up Virtual Environment."""
    print green("***" * 27)
    print green("*** Going to set up Virtual Environment...")

    with cd("{app_folder}".format(
            app_folder=env.app_folder,
            )):
        run("virtualenv ve --no-site-packages")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_ve_reqs_install():
    """Install the Project Requirements."""
    print green("***" * 27)
    print green("*** Going to install the Project Requirements...")

    with cd("{app_folder}".format(
            app_folder=env.app_folder,
            )):
        with prefix("{ve_activate}".format(
                ve_activate=env.ve_activate,
                )):
            run("pip install --no-cache-dir -r {requirements_file}".format(
                requirements_file=env.requirements_file,
                ))

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_env_vars_export():
    """Export Environment Variables."""
    print green("***" * 27)
    print green("*** Going to export Environment Variables...")

    sudo("echo \"\" >> ~/.profile")
    sudo("echo \"# Custom Environment Variables\" >> ~/.profile")

    for key, value in env.variables[env.environment].items():
        sudo("echo \"export {key}={value}\" >> ~/.profile".format(
            key=key,
            value=value,
            ))

    sudo("source ~/.profile")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_project_setup():
    """Set up the Project."""
    print green("***" * 27)
    print green("*** Going to set up the Project...")

    with cd("{app_folder}/src".format(
            app_folder=env.app_folder,
            )):
        with prefix("{ve_activate}".format(
                ve_activate=env.ve_activate,
                )):
            run("python manage.py migrate --fake-initial")
            run("python manage.py migrate")
            run("python manage.py bower install")

            with settings(warn_only=True):
                run("python manage.py collectstatic")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_project_setup_symlinks():
    """Set up the Project SymLinks."""
    run("mkdir {app_folder}/src/staticserve/CACHE/".format(app_folder=env.app_folder))
    run("mkdir {app_folder}/src/staticserve/CACHE/img/".format(app_folder=env.app_folder))
    run(
        "ln -s {src_dir}/src/static/img/ "
        "{dst_dir}/src/staticserve/CACHE/img/".format(
            src_dir=env.app_folder,
            dst_dir=env.app_folder))

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_cache_fv_setup():
    """Set up Django Cache Framework."""
    print green("***" * 27)
    print green("*** Going to set up Django Cache Framework...")

    with cd("{app_folder}/src".format(
            app_folder=env.app_folder,
            )):
        with prefix("{ve_activate}".format(
                ve_activate=env.ve_activate,
                )):
            run("python manage.py createcachetable")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_cache_clear():
    """Clear Django Cache."""
    print green("***" * 27)
    print green("*** Going to clear Django Cache...")

    with cd("{app_folder}/src".format(
            app_folder=env.app_folder,
            )):
        with prefix("{ve_activate}".format(
                ve_activate=env.ve_activate,
                )):
            run("python manage.py clear_cache")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_seo_fv_setup():
    """Set up Django SEO Framework."""
    print green("***" * 27)
    print green("*** Going to set up Django SEO Framework...")

    with cd("{app_folder}/src".format(app_folder=env.app_folder)):
        with prefix("{ve_activate}".format(ve_activate=env.ve_activate)):
            run("python manage.py makemigrations djangoseo")
            run("python manage.py migrate djangoseo --fake-initial")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_elasticsearch_setup():
    """Set up ElasticSearch."""
    print green("***" * 27)
    print green("*** Going to set up ElasticSearch...")

    # -------------------------------------------------------------------------
    # --- Install Java VM
    print cyan("[---  INFO   ---] Install Java VM...")

    # --- Should be implemented manually for now
    # sudo("apt-get install    -y python-software-properties")
    # sudo("add-apt-repository -y ppa:webupd8team/java")
    # sudo("apt-get update")
    # sudo("apt-get install    -y oracle-java8-installer")

    print yellow("[--- WARNING ---] Skip this Step...")

    # -------------------------------------------------------------------------
    # --- Download and install the Public Signing Key
    print cyan("[---  INFO   ---] Download and install the Public Signing Key...")

    sudo(
        "wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch "
        "| sudo apt-key add -")
    sudo(
        "echo \"deb http://packages.elastic.co/elasticsearch/2.x/debian "
        "stable main\" "
        "| sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list")

    # -------------------------------------------------------------------------
    # --- Install & run ElasticSearch
    print cyan("[---  INFO   ---] Install & run ElasticSearch...")

    sudo("apt-get update")
    sudo("apt-get install -y elasticsearch")
    sudo("service elasticsearch start")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_elasticsearch_restart():
    """Restart ElasticSearch."""
    print green("***" * 27)
    print green("*** Going to restart ElasticSearch...")

    sudo("service elasticsearch restart")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_elasticsearch_rebuild_indexes():
    """Rebuild Search Indexes."""
    print green("***" * 27)
    print green("*** Going to rebuild Search Indexes...")

    with cd("{app_folder}/src".format(app_folder=env.app_folder)):
        with prefix("{ve_activate}".format(ve_activate=env.ve_activate)):
            run("python manage.py rebuild_index -v2")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_make_messages():
    """Make locale Messages."""
    print green("***" * 27)
    print green("*** Going to make locale Messages...")

    with cd("{app_folder}/src".format(app_folder=env.app_folder)):
        with prefix("{ve_activate}".format(ve_activate=env.ve_activate)):
            with settings(warn_only=True):
                run("python manage.py makemessages -l de")
                run("python manage.py makemessages -l es")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def app_compile_messages():
    """Compile locale Messages."""
    print green("***" * 27)
    print green("*** Going to compile locale Messages...")

    with cd("{app_folder}/src".format(app_folder=env.app_folder)):
        with prefix("{ve_activate}".format(ve_activate=env.ve_activate)):
            with settings(warn_only=True):
                run("python manage.py compilemessages -l de")
                run("python manage.py compilemessages -l es")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def uwsgi_setup():
    """Set up uWSGI."""
    print green("***" * 27)
    print green("*** Going to set up uWSGI...")

    # -------------------------------------------------------------------------
    # --- Install uWSGI
    print cyan("[---  INFO   ---] Install uWSGI...")

    with prefix("{ve_activate}".format(ve_activate=env.ve_activate)):
        sudo("pip install uwsgi")

    # -------------------------------------------------------------------------
    # --- Copy uWSGI Configuration File
    print cyan("[---  INFO   ---] Copy uWSGI Configuration File...")

    sudo(
        "cp -u "
        "{app_folder}/deployment/{environment}/uwsgi/etc/init/uwsgi.conf "
        "/etc/init/".format(
            app_folder=env.app_folder,
            environment=env.environment))

    with settings(warn_only=True):
        sudo("ln /usr/local/bin/uwsgi /usr/bin/uwsgi")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def uwsgi_restart():
    """Restart uWSGI."""
    print green("***" * 27)
    print green("*** Going to restart uWSGI...")

    with settings(warn_only=True):
        sudo("stop  uwsgi")
        sudo("start uwsgi")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def nginx_setup():
    """Set up Nginx."""
    print green("***" * 27)
    print green("*** Going to set up Nginx...")

    # -------------------------------------------------------------------------
    # --- Install Nginx
    print cyan("[---  INFO   ---] Install Nginx...")

    sudo("apt-get install -y nginx")

    with settings(warn_only=True):
        run("mkdir /opt/nginx")
        run("mkdir /opt/nginx/{sites-available,sites-enabled}")

    sudo(
        "sed -i \"s/include "
        "\/etc\/nginx\/sites-enabled/include "
        "\/opt\/nginx\/sites-enabled/g\" /etc/nginx/nginx.conf")
    # -------------------------------------------------------------------------
    # --- Copy Nginx Configuration File
    print cyan("[---  INFO   ---] Copy Nginx Configuration File...")

    sudo(
        "cp -u "
        "{app_folder}/deployment/{environment}/nginx/sites-available/saneside "
        "/opt/nginx/sites-available/".format(
            app_folder=env.app_folder,
            environment=env.environment,
            ))

    with settings(warn_only=True):
        run(
            "ln -s "
            "/opt/nginx/sites-available/saneside "
            "/opt/nginx/sites-enabled/saneside")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


def nginx_restart():
    """Restart Nginx."""
    print green("***" * 27)
    print green("*** Going to restart Nginx...")

    with settings(warn_only=True):
        sudo("/etc/init.d/nginx restart")

    print cyan("[---  INFO   ---] STEP COMPLETE")
    _spinner_sleep(delay=1, step=0.1)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ---
# --- DEPLOY
# ---
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def deploy():
    """Deploy the Project from Scratch."""
    print green("***" * 27)
    print green("*** Going to deploy the Project from Scratch...")

    print cyan("[---  INFO   ---] ENVIRONMENT : %s" % env.environment)

    _spinner_sleep(delay=2, step=0.1)

    apt_upgrade()
    apt_install()
    apt_install_mysql()

    npm_install()

    app_wd_create()
    app_git_clone()
    app_git_pull()
    app_ve_install()
    app_ve_reqs_install()
    app_env_vars_export()
    app_project_setup()
    app_project_setup_symlinks()
    app_cache_fv_setup()
    app_cache_clear()
    app_seo_fv_setup()
    app_elasticsearch_setup()
    app_elasticsearch_rebuild_indexes()
    # app_make_messages()
    app_compile_messages()

    uwsgi_setup()
    uwsgi_restart()

    nginx_setup()
    nginx_restart()

    print green("DONE!")


def update():
    """Update the Project."""
    print green("***" * 27)
    print green("*** Going to update the Project...")

    print cyan("[---  INFO   ---] ENVIRONMENT : %s" % env.environment)

    apt_upgrade()
    npm_upgrade()

    app_git_pull()
    app_ve_reqs_install()
    app_project_setup()
    app_cache_clear()
    app_elasticsearch_restart()
    app_elasticsearch_rebuild_indexes()
    # app_make_messages()
    app_compile_messages()

    uwsgi_restart()

    nginx_restart()

    print green("DONE!")


def restart():
    """Restart the Project."""
    print green("***" * 27)
    print green("*** Going to restart the Project...")

    print cyan("[---  INFO   ---] ENVIRONMENT : %s" % env.environment)

    app_cache_clear()

    app_elasticsearch_restart()
    app_elasticsearch_rebuild_indexes()

    uwsgi_restart()

    nginx_restart()

    print green("DONE!")


def stop():
    """Stop the Project."""
    print green("***" * 27)
    print green("*** Going to stop the Project...")

    print cyan("[---  INFO   ---] ENVIRONMENT : %s" % env.environment)

    print green("DONE!")
