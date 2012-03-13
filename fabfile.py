from fabric.api import cd, local, env, run


env.hosts = ['nick@beta.snipt.net:39039']
env.site_path = '/var/www/snipt'
env.venv_path = '/home/nick/.virtualenvs/snipt'

def _python(cmd):
    return env.venv_path.rstrip('/') + '/bin/python ' + cmd

def deploy(m):
    local('python manage.py collectstatic --ignore grappelli --ignore admin --noinput')

    try:
        local("hg commit -m '{}'".format(m))
    except:
        pass
    local('hg push')

    with cd(env.site_path):
        run('hg pull -u')
        run(_python('manage.py collectstatic --ignore grappelli --ignore admin --noinput'))


