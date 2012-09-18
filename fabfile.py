from fabric.api import cd, local, env, run

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import datetime, sys


env.hosts = ['nick@snipt.net:39039']
env.site_path = '/var/www/snipt'
env.venv_path = '/home/nick/.virtualenvs/snipt'

def _python(cmd):
    return env.venv_path.rstrip('/') + '/bin/python ' + cmd

def dep():

    _display_message('Compiling CSS')
    ################

    local('scss -t compressed media/css/style.scss media/css/style.css')
    local('scss -t compressed media/css/blog-themes/default/style.scss media/css/blog-themes/default/style.css')
    local('scss -t compressed media/css/blog-themes/pro-adams/style.scss media/css/blog-themes/pro-adams/style.css')
    local('media/css/compile-css.sh')

    local('git commit -am "Compiling CSS"')

    _display_message('Collect static')
    ################

    local('python manage.py collectstatic --ignore cache --noinput')

    _display_message('Git push')
    ################

    try:
        local('git push')

        _display_message('Get last commit info')
        ################

        local('./get-last-commit-url.py')
    except:
        pass

    print('')

    with cd(env.site_path):

        _display_message('Git pull')
        ################

        run('git pull')

        _display_message('Collect static', False)
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

        run('./gk')

        _display_message('Restart gunicorn process')
        ################

        run('/home/nick/.virtualenvs/snipt/bin/python /home/nick/.virtualenvs/snipt/bin/gunicorn -c gunicorn.conf.py debug_wsgi:application')

def db_backup():

    filename = datetime.datetime.now().strftime('%h-%d-%y__%I-%M-%S_%p.pgdump')

    local('pg_dump snipt > {}'.format(filename))

    conn = S3Connection('AKIAJJRRQPTSPKB7GYOA', 'DIYz2g5vPjcWE4/YI7wEuUVAskwJxs2llFvGyI1a')
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

