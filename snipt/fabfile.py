import os

from fabric.api import local

def staticfiles():
    BASE_PATH = os.path.dirname(__file__)

    # CSS
    local('sass %s/media/css/style.scss %s/media/css/style.css' % (BASE_PATH, BASE_PATH))
    local('sed -i -e \'s/\/media\//https:\/\/snipt.s3.amazonaws.com\//g\' %s/media/css/style.css' % BASE_PATH)
    local('rm %s/media/css/style.css-e' % BASE_PATH)
    css = [
        '%s/media/css/bootstrap.css' % BASE_PATH,
        '%s/media/css/style.css' % BASE_PATH,
        '%s/media/css/themes.css' % BASE_PATH,
    ]
    local('cat %s > %s/media/cache/snipt.css' % (' '.join(css), BASE_PATH))
    
    # JS
    js = [
        '%s/media/js/libs/underscore.js' % BASE_PATH,
        '%s/media/js/libs/jquery.js' % BASE_PATH,
        '%s/media/js/libs/json2.js' % BASE_PATH,
        '%s/media/js/libs/backbone.js' % BASE_PATH,
        '%s/media/js/libs/bootstrap.js' % BASE_PATH,

        '%s/media/js/plugins/jquery.hotkeys.js' % BASE_PATH,
        '%s/media/js/plugins/jquery.infieldlabel.js' % BASE_PATH,
        '%s/media/js/plugins/jquery.ui.js' % BASE_PATH,

        '%s/media/js/src/application.js' % BASE_PATH,
        '%s/media/js/src/modules/site.js' % BASE_PATH,
        '%s/media/js/src/modules/snipt.js' % BASE_PATH,
    ]
    local('cat %s > %s/media/cache/snipt.js' % (' '.join(js), BASE_PATH))
    local('/Users/Nick/.virtualenvs/snipt/bin/python %s/manage.py collectstatic --ignore grappelli --ignore admin --ignore ace --noinput' % BASE_PATH)

def deployapp(m):
    try:
        local('hg commit -m \'%s\'' % m)
    except:
        pass
    try:
        local('git add .')
        local('git commit -m \'%s\'' % m)
    except:
        pass
    local('hg push')
    local('git push -f heroku')
    local('heroku restart')

def deploy(m):
    staticfiles()
    deployapp(m)

def deployall(m):
    deploy(m)
    local('heroku run bin/python snipt/manage.py syncdb')
    local('heroku run bin/python snipt/manage.py migrate')
