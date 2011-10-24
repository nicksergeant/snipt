import os

from fabric.api import local

def staticfiles():
    BASE_PATH = os.path.dirname(__file__)
    local('lessc %s/media/css/style.less %s/media/css/style.css' % (BASE_PATH, BASE_PATH))
    local('coffee -c %s/media/js/script.coffee' % BASE_PATH)
    local('%s/manage.py collectstatic' % BASE_PATH)

def deployall():
    staticfiles()
    deployapp()

def deployapp():
    local('hg push')
    local('hg push-heroku')
