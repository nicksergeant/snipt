# Snipt

This is the codebase for the website, [Snipt.net](https://snipt.net/).

# Running the Django app locally with Vagrant

Install [Vagrant](https://www.vagrantup.com/) and either [VirtualBox](https://www.virtualbox.org/) or
[VMWare Fusion](http://www.vmware.com/products/fusion).

1. Clone the repo.
2. `cp settings_local.py-template settings_local.py`
3. Edit local settings (choose a database password - you'll be prompted for it).
4. `make vagrant`
5. Visit [http://local.snipt.net:8080/](http://local.snipt.net:8080/).

# Deploying to a VM

1. Clone the repo.
2. `cp settings_local.py-template settings_local_server.py`
3. Edit local server settings (choose a database password - you'll be prompted for it).
4. Manually change the VM IP address in the Makefile.
5. `make server`
6. SSH into the server, `sudo su - deploy`, `ssh-keygen`, and add the public key to your repo as a deploy key.
7. `make server-init`

# Deploying to Heroku

1. Clone the repo.
2. `heroku create`
3. `heroku addons:add heroku-postgresql:hobby-dev`
4. `heroku addons:add searchbox`
8. `heroku config:add DEBUG=False`
9. `heroku config:add INTERCOM_SECRET_KEY=`
9. `heroku config:add POSTMARK_API_KEY=`
11. `heroku config:add RAVEN_CONFIG_DSN=`
12. `heroku config:add SECRET_KEY=`
13. `heroku config:add STRIPE_SECRET_KEY=`
14. `heroku config:add USE_SSL=False`
15. `git push heroku`
16. `heroku run python manage.py syncdb`
17. `heroku run python manage.py migrate`

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
