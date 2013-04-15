#!/usr/bin/env python
# -- coding: utf-8 --

from fabric.api import cd, local, env, run, sudo

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import datetime, hashlib, sys

from settings_local import AMAZON_API_KEY, AMAZON_API_SECRET, ENV_HOST


env.hosts = [ENV_HOST]
env.site_path = '/var/www/snipt'
env.venv_path = '/home/nick/.virtualenvs/snipt'

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

def db_backup():

    filename = datetime.datetime.now().strftime('%h-%d-%y__%I-%M-%S_%p.pgdump')

    local('pg_dump snipt > {}'.format(filename))

    conn = S3Connection(AMAZON_API_KEY, AMAZON_API_SECRET)
    snipt_bucket = conn.get_bucket('snipt')

    k = Key(snipt_bucket)
    k.key = filename
    k.set_contents_from_filename(filename)

    local('rm {}'.format(filename))

def db():
    with cd(env.site_path):

        _display_message('Sync DB and migrate')
        ################

        run(_python('manage.py syncdb'))
        run(_python('manage.py migrate'))

def gravatars():

    from fabric.contrib import django
    django.settings_module('settings')

    from django.contrib.auth.models import User

    import requests

    _display_message('Updating all users\' Gravatar flags')
    ################

    for user in User.objects.all().order_by('id'):

        _display_message('{}. {}'.format(user.pk, user.username.encode('ascii', 'ignore')))
        ################

        email_md5 = hashlib.md5(user.email.lower()).hexdigest()

        print 'Email MD5: {}'.format(email_md5)

        greq = requests.get('https://secure.gravatar.com/avatar/{}?s=50&d=404'.format(email_md5))

        if greq.status_code == 404:
            has_gravatar = False
        else:
            has_gravatar = True

        profile = user.profile
        profile.has_gravatar = has_gravatar
        profile.save()

        try:
            from fabric.colors import green, red

            if has_gravatar:
                print 'Has Gravatar: {}'.format(green(has_gravatar))
            else:
                print 'Has Gravatar: {}'.format(red(has_gravatar))

        except ImportError:
            print 'Has Gravatar: {}'.format(has_gravatar)

def re():
    with cd(env.site_path):

        _display_message('Kill gunicorn process')
        ################

        sudo('supervisorctl stop snipt')

        _display_message('Restart gunicorn process')
        ################

        sudo('supervisorctl start snipt')

