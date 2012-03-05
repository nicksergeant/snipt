import os

from fabric.api import local

def staticfiles():
    BASE_PATH = os.path.dirname(__file__)

    # CSS
    local('sass %s/media/css/style.scss %s/media/css/style.css' % (BASE_PATH, BASE_PATH))
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
    local('/Users/Nick/.virtualenvs/snipt/bin/python %s/manage.py collectstatic --ignore grappelli --ignore admin --noinput' % BASE_PATH)

def deploy(m):
    staticfiles()

    try:
        local('hg commit -m \'%s\'' % m)
    except:
        pass

    local('hg push')

    run('hg pull -u')
    run('python manage.py collectstatic --ignore grappelli --ignore admin --noinput')
