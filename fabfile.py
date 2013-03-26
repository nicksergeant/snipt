from fabric.api import cd, local, env, run, sudo

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import datetime, sys

from settings_local import AMAZON_API_KEY, AMAZON_API_SECRET, ENV_HOST


env.hosts = [ENV_HOST]
env.site_path = '/var/www/snipt'
env.venv_path = '/home/nick/.virtualenvs/snipt'

def _python(cmd):
    return env.venv_path.rstrip('/') + '/bin/python ' + cmd

def dep():

    _display_message('Collect static (local)')
    ################

    local('python manage.py collectstatic --ignore cache --noinput')

    _display_message('Git push')
    ################

    try:
        local('git push')

        _display_message('Get last commit info')
        ################

    except:
        pass

    print('')

    with cd(env.site_path):

        _display_message('Git pull')
        ################

        run('git pull')

        _display_message('Collect static (remote)', False)
        ################

        run(_python('manage.py collectstatic --ignore cache --noinput'))

def db():
    with cd(env.site_path):

        _display_message('Sync DB and migrate')
        ################

        run(_python('manage.py syncdb'))
        run(_python('manage.py migrate'))

def re():
    with cd(env.site_path):

        _display_message('Kill gunicorn process')
        ################

        sudo('supervisorctl stop snipt')

        _display_message('Restart gunicorn process')
        ################

        sudo('supervisorctl start snipt')

def db_backup():

    filename = datetime.datetime.now().strftime('%h-%d-%y__%I-%M-%S_%p.pgdump')

    local('pg_dump snipt > {}'.format(filename))

    conn = S3Connection(AMAZON_API_KEY, AMAZON_API_SECRET)
    snipt_bucket = conn.get_bucket('snipt')

    k = Key(snipt_bucket)
    k.key = filename
    k.set_contents_from_filename(filename)

    local('rm {}'.format(filename))

def _display_message(message, extra_line=True):
    if extra_line:
        msg = '\n{}\n========================\n\n'.format(message)
    else:
        msg = '{}\n========================\n\n'.format(message)
    try:
        from fabric.colors import cyan
        sys.stderr.write(cyan(msg))
    except ImportError:
        print(msg)

