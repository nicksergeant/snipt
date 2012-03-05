from fabric.api import cd, local, env, run


env.hosts = ['nick@beta.snipt.net:39039']
env.site_path = '/var/www/snipt'

def deploy():
    local('python manage.py collectstatic --ignore grappelli --ignore admin --noinput')
    with cd(env.site_path):
        run('hg pull -u')
        run('python manage.py collectstatic --ignore grappelli --ignore admin --noinput')
