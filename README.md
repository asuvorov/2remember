# Table of Contents
For more Information on how to work in the Project, check out some of the other Documentation provided:
<!--ts-->
* [Building](docs/BUILDING.md)
* [Contributing](docs/CONTRIBUTING.md)
* [Developer](docs/CDEVELOPER.md)
* [Telemetry](docs/TELEMETRY.md)
<!--te-->

# Install Dependencies

## Install `node` and `npm`

1. MacOS

		brew install nodejs npm

2. Ubuntu

		apt-get install -y nodejs nodejs-legacy npm

	```
	npm cache clear
	npm update npm -g
	npm config set registry http://registry.npmjs.org/
	```

## Install `bower`

	npm install -g bower

### Download and install `bower` Applications

	python manage.py bower install 

## Install `lessc` (and optional `recess`):

	npm install -g less recess

# Internationalization

## Install `gettext`

1. MacOS

		brew install gettext
		brew link gettext --force

2. Ubuntu

		sudo apt install gettext

## Generate and compile Message Files

	python manage.py makemessages    -l <locale>
	python manage.py compilemessages -l <locale>

## [See also](http://www.marinamele.com/taskbuster-django-tutorial/internationalization-localization-languages-time-zones)

# Connecting to AWS Resources

1. `EC2` Instance - Staging

		ssh -i ~/.ssh/UbuntuHome.pem ubuntu@54.200.235.210

1. `EC2` Instance - Production

		ssh -i ~/.ssh/UbuntuHome.pem ubuntu@34.220.216.17

1. `RDS` Instance

		mysql -h saneside.csisnutyjpxo.us-west-2.rds.amazonaws.com -P 3306 -u saneside_admin -p
