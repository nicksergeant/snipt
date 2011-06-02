from __future__ import with_statement

import os
from fabric.api import *
from dwfab.misc import growl as _growl


UPLOADS_DIR = 'media/uploads'
APPS_TO_SYNC = [
    'auth',
    'contenttypes',
    'redirects',
    'registration',
]

def prod():
    '''Run on the production site.'''
    env.env_name = 'production'
    env.hosts = ['nick@beta.snipt.net:38038']
    env.process_name = 'beta-snipt'
    env.site_path = '/var/www/beta-snipt'
    env.venv_path = '/home/nick/.virtualenvs/beta-snipt'
    env.site_url = 'https://beta.snipt.net/'
    env.uploads_path = env.site_path + '/' + UPLOADS_DIR


def _python(cmd):
    return env.venv_path.rstrip('/') + '/bin/python ' + cmd
def _lpython(cmd):
    return os.getenv('VIRTUAL_ENV').rstrip('/') + '/bin/python ' + cmd
def _pip(cmd):
    return env.venv_path.rstrip('/') + '/bin/pip ' + cmd


def pull_uploads():
    '''Copy the uploads from the site to your local machine.'''
    require('uploads_path', provided_by=['prod'])

    sudo('chmod -R a+r "%s"' % env.uploads_path)

    rsync_command = r"""rsync -av -e 'ssh -p %s' %s@%s:%s %s""" % (
        env.port,
        env.user, env.host,
        env.uploads_path.rstrip('/') + '/',
        UPLOADS_DIR.rstrip('/')
    )
    print local(rsync_command, capture=False)

def pull_data():
    '''Copy the data from the site to your local machine.'''
    require('site_path', provided_by=['prod'])
    require('venv_path', provided_by=['prod'])

    for app in APPS_TO_SYNC:
        local(_lpython('manage.py reset --noinput %s' % app))
        local(_lpython('manage.py migrate --fake %s' % app))

    for app in APPS_TO_SYNC:
        with cd(env.site_path):
            sudo(_python('manage.py dumpdata --format=json --indent=2 --natural ' +
                        '%s > snipt-fixtures-%s.json' % (app, app)))
        get('%s/snipt-fixtures-%s.json' % (env.site_path, app), 'snipt-fixtures-%s.json' % app)

        local(_lpython('manage.py loaddata snipt-fixtures-%s.json' % app))

def pull_all():
    '''Copy the uploads and data from the site to your local machine.'''
    pull_uploads()
    pull_data()
    _growl('Snipt: Pull Complete', 'The database and uploads have been refreshed.')


def reindex():
    require('site_path', provided_by=['prod'])

    with cd(env.site_path):
        sudo(_python('manage.py rebuild_index --noinput'))


def syncdb():
    '''Run syncdb.'''
    require('site_path', provided_by=['prod'])
    require('venv_path', provided_by=['prod'])

    with cd(env.site_path):
        sudo(_python('manage.py syncdb'))

def migrate():
    '''Run any needed migrations.'''
    require('site_path', provided_by=['prod'])
    require('venv_path', provided_by=['prod'])

    with cd(env.site_path):
        sudo(_python('manage.py migrate'))

def requirements():
    '''Copy local requirements.txt to the site and install requirements.'''
    require('site_path', provided_by=['prod'])
    require('venv_path', provided_by=['prod'])

    with cd(env.site_path):
        put('requirements.txt', 'requirements.txt')
        run(_pip('install -r requirements.txt'))
        run('hg revert requirements.txt')


def retag():
    '''Check which revision the site is at and update the local tag.

    Useful if someone else has deployed (which makes your production/staging local
    tag incorrect.
    '''
    require('site_path', provided_by=['prod'])
    require('env_name', provided_by=['prod'])

    with cd(env.site_path):
        current = run('hg id --rev . --quiet').strip(' \n+')

    local('hg tag --local --force %s --rev %s' % (env.env_name, current))

def deploy(rev='.'):
    '''Deploy your current revision to the site.
    
    You can also specify a different revision to deploy by passing an argument:

        fab stag deploy:1a2cc06d

    You can use your local revision numbers as arguments -- the full hash will be
    looked up and used.
    '''
    require('site_path', provided_by=['prod'])

    rev = local('hg id --rev %s --quiet' % rev).strip(' \n+')

    local('hg push --rev %s' % rev)

    with cd(env.site_path):
        run('hg tag --local --force previous')
        run('hg pull --rev %s' % rev)
        run('hg update --rev %s' % rev)

    retag()

    syncdb()
    migrate()

    restart()
    check()


def deploy_template(rev='.'):
    '''Deploy your current revision to the site, without restarting the server.
    
    You can also specify a different revision to deploy by passing an argument:

        fab stag deploy:1a2cc06d

    You can use your local revision numbers as arguments -- the full hash will be
    looked up and used.
    '''
    require('site_path', provided_by=['prod'])

    rev = local('hg id --rev %s --quiet' % rev).strip(' \n+')

    local('hg push --rev %s' % rev)

    with cd(env.site_path):
        run('hg tag --local --force previous')
        run('hg pull --rev %s' % rev)
        run('hg update --rev %s' % rev)

    retag()
    check()


def rollback():
    '''Roll the site back to the version it was at before the last deployment.
    
    Things may break if migrations were made between the versions. TODO: Fix this.
    '''
    require('site_path', provided_by=['prod'])

    with cd(env.site_path):
        run('hg update previous')

    retag()
    restart()
    check()

def check():
    '''Check that the home page of the site returns an HTTP 200.
    
    If it does, a normal growl message is sent.

    If it does not, a warning is issued and a sticky growl message is sent.
    '''
    require('site_url', provided_by=['prod'])

    if not '200 OK' in run('curl --silent -I "%s"' % env.site_url):
        warn("Something is wrong (we didn't get a 200 response)!")
        _growl('Snipt: DEPLOYMENT ERROR', 'Something went wrong. Please investigate.', sticky=True)
    else:
        _growl('Snipt: Deployment Complete', 'Deployment finished, site is working.')

def restart():
    '''Restart the site's gunicorn server.'''
    require('site_path', provided_by=['prod'])
    require('process_name', provided_by=['prod'])

    sudo('supervisorctl restart %s' % env.process_name)

    with cd(env.site_path):
        sudo('chmod a+r media/css/*.css')


