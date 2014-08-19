
Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv
* postgresql
* libpq-dev
* python3.4-dev
* psycopg2


eg, on Ubuntu:
    sudo aptitude install nginx git python3 python3-pip
    sudo aptitude install libpq-dev python3.4-dev
    sudo pip3 install virtualenv

## PostgreSQL 9.3

* how to install postgresql-9.3 on Ubuntu 12.04 (precise), default was 9.1
    sudo bash
    echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
    exit
    sudo aptitude install wget
    sudo aptitude install ca-certificates
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo aptitude update
    sudo aptitude upgrade
    sudo aptitude install postgresql-9.3

* how to configure postgresql to allow password login from the 'postgres' user
    $ sudo su postgres
    $ psql -U postgres
within psql change postgres user password
    # ALTER ROLE postgres PASSWORD 'secret_word';
    # \q
now edit pg_hba.conf to allow password/md5 login for this user
    $ sudo emacs /etc/postgresql/9.3/main/pg_hba.conf

* how to add a new user for our app
    $ createuser -U postgres -d -P APP_USER
provide first the new user password twice, then the postgres password
    $ createdb -U postgres APP_DATABASE_NAME



## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv

