from fabric.contrib.files import append, exists, sed, comment
from fabric.api import env, local, run, settings, sudo
import random

REPO_URL = 'https://github.com/ashleywinn/webtranslate.git'


def deploy():
  site_folder = '/home/%s/sites/%s' % (env.user, env.host)
  source_folder = site_folder + '/source'
  _create_directory_structure_if_necessary(site_folder)
  _get_latest_source(source_folder)
  _update_settings(source_folder, env.host)
  _update_virtualenv(source_folder)
  _update_static_files(source_folder)
  _update_database(source_folder)
  _restart_gunicorn(env.host)

def load_hsk_words():
  source_folder = '/home/%s/sites/%s/source' % (env.user, env.host)
  run('cd %s && ../venv/bin/python manage.py load_hsk_lists' % (source_folder,))


def _create_postgres_user(username, pwd):
  with settings(prompts={'Enter password for new role: ' : pwd,
                         'Enter it again: ' : pwd}):
    run('createuser --pwprompt --createdb %s' % (username,))
    run('createdb %s' % (username,))
  
  
def _create_directory_structure_if_necessary(site_folder):
  for subfolder in ('static', 'venv', 'source'):
    run('mkdir -p %s/%s' % (site_folder, subfolder))
    
def _get_latest_source(source_folder):
  if exists(source_folder + '/.git'):
    run('cd %s && git fetch' % (source_folder,))
  else:
    run('git clone %s %s' % (REPO_URL, source_folder))
  current_commit = local("git log -n 1 --format=%H", capture=True)
  run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _create_secrets_file(secrets_file, site_name):
  if not exists(secrets_file):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    db_user = site_name.replace('.','').replace('-','')
    db_pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(40))
    django_key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    _create_postgres_user(db_user, db_pwd)
    append(secrets_file,  "SECRET_KEY = '%s'" % (django_key,))
    append(secrets_file,  "DATABASES = {")
    append(secrets_file,  "    'default': {")
    append(secrets_file,  "          'ENGINE': 'django.db.backends.postgresql_psycopg2',")
    append(secrets_file,  "            'NAME': '%s'," % (db_user,))
    append(secrets_file,  "            'USER': '%s'," % (db_user,))
    append(secrets_file,  "        'PASSWORD': '%s'," % (db_pwd,))
    append(secrets_file,  "    }")
    append(secrets_file,  "}")

def _comment_databases_setting(settings_file):
  comment(settings_file, '''DATABASES =''', char='# ') # {"default':{''')
  comment(settings_file, '''\s+"ENGINE": "django.db.backends.postgresql_psycopg2",''')
  comment(settings_file, '''\s+"NAME": "django_putonghua_db",''')
  comment(settings_file, '''\s+"USER": "django_putonghua",''')
  comment(settings_file, '''\s+"PASSWORD": "froumlesefjamgxo"}}''')

  
def _update_settings(source_folder, site_name):
  settings_path = source_folder + '/webtranslate/settings.py'
  sed(settings_path, "DEBUG = True", "DEBUG = False")
  
  allowed_host = site_name
  # hack to allow www.example.com a domain to also match example.com
  if allowed_host.startswith('www'):
    allowed_host = allowed_host[3:]  # remove the 'www' so its just '.example.com'
  sed(settings_path,
      'ALLOWED_HOSTS =.+$',
      'ALLOWED_HOSTS = ["%s"]' % (allowed_host,)
      )
  comment(settings_path, "SECRET_KEY =")
  _comment_databases_setting(settings_path)
  secrets_file = source_folder + '/webtranslate/secrets.py'
  if not exists(secrets_file):
    _create_secrets_file(secrets_file, site_name)
  append(settings_path, '\nfrom .secrets import SECRET_KEY')
  append(settings_path, '\nfrom .secrets import DATABASES')
  
def _update_virtualenv(source_folder):
  virtualenv_folder = source_folder + '/../venv'
  if not exists(virtualenv_folder + '/bin/pip'):
    run('virtualenv --python=python3.4 %s' % (virtualenv_folder,))
  run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder))
        
def _update_static_files(source_folder):
  run('cd %s && ../venv/bin/python manage.py collectstatic --noinput' % (
      source_folder,))
      
def _update_database(source_folder):
  run('cd %s && ../venv/bin/python manage.py migrate --noinput' % (
      source_folder,))
  run('cd %s && ../venv/bin/python manage.py do_db_updates' % (
      source_folder,))


def _restart_gunicorn(site_name):
  sudo('service gunicorn-%s restart' % (site_name,))
