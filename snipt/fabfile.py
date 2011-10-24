import os

from fabric.api import local

def staticfiles():
    BASE_PATH = os.path.dirname(__file__)
    local('lessc %s/media/css/style.less %s/media/css/style.css' % (BASE_PATH, BASE_PATH))
    local('coffee -c %s/media/js/script.coffee' % BASE_PATH)
    local('sed -i -e \'s/\/media\//https:\/\/dn2p0mzo970os.cloudfront.net\//g\' %s/media/css/style.css' % BASE_PATH)
    local('rm %s/media/css/style.css-e' % BASE_PATH)
    local('cat %s/media/css/*.css > %s/media/cache/snipt.css' % (BASE_PATH, BASE_PATH))
    local('cat %s/media/js/jquery.js %s/media/js/jquery.*.js %s/media/js/script.js > %s/media/cache/snipt.js' % (BASE_PATH, BASE_PATH, BASE_PATH, BASE_PATH))
    try:
        local('hg commit -m "Autocommit by [fab staticfiles]"')
        local('hg push')
    except:
        pass
    local('%s/manage.py collectstatic' % BASE_PATH)

def deployall():
    staticfiles()
    deployapp()

def deployapp():
    local('hg push')
    local('hg push-heroku')
