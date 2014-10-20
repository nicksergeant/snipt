#!/usr/bin/env python
# -- coding: utf-8 --

from fabric.api import cd, local, env, run, sudo

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import datetime, hashlib, sys

from settings_local import AMAZON_API_KEY, AMAZON_API_SECRET, ENV_HOST


env.hosts = [ENV_HOST]
env.site_path = '/home/nick/snipt'


def dep():
    local('python manage.py collectstatic --ignore cache --noinput')

    try:
        local('git push')
    except:
        pass

    with cd(env.site_path):
        run('git pull')
        run('/home/nick/snipt/.docker/control.sh collectstatic')
        run('/home/nick/snipt/.docker/control.sh deploy')

def db_backup():
    filename = datetime.datetime.now().strftime('%h-%d-%y__%I-%M-%S_%p.pgdump')
    path = '/tmp/{}'.format(filename)
    local('/home/nick/snipt/.docker/control.sh backupdb > {}'.format(path))
    conn = S3Connection(AMAZON_API_KEY, AMAZON_API_SECRET)
    snipt_bucket = conn.get_bucket('snipt')
    k = Key(snipt_bucket)
    k.key = filename
    k.set_contents_from_filename(filename)
    local('rm {}'.format(path))

def db():
    with cd(env.site_path):
        run('/home/nick/snipt/.docker/control.sh syncdb')
        run('/home/nick/snipt/.docker/control.sh migrate')

def gravatars():

    from fabric.contrib import django
    django.settings_module('settings')

    from django.contrib.auth.models import User

    import requests

    for user in User.objects.all().order_by('id'):

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
        run('/home/nick/snipt/.docker/control.sh restart')
