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

# Deploying to Heroku

- Clone the repo.
- `heroku create`
- `heroku addons:add heroku-postgresql:hobby-dev`
- `heroku addons:add searchbox`
- `heroku addons:create postmark:10k`
- `heroku addons:open postmark` -> use an email you control
- `heroku config:add POSTMARK_EMAIL=<email_from_above>`
- `heroku config:add DEBUG=False`
- `heroku config:add SECRET_KEY=`
- `git push heroku`
- `heroku run python manage.py migrate`
- `heroku run python manage.py createsuperuser`
- Visit yourapp.herokuapp.com and login with the user you just created.

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
