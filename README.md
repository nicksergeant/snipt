# Snipt

## Running locally

- Clone the repo.
- `cd snipt`
- `python3 -m venv ~/.virtualenvs/snipt`
- `source ~/.virtualenvs/snipt/bin/activate`
- `pip install -r requirements.txt`
- `brew install postgresql`
- `brew services start postgresql`
- `createuser snipt`
- `createdb snipt --owner=snipt`
- `cp settings_local.py-template settings_local.py` // modify if necessary
- `make run`

## Deploying on Dokku

- `dokku apps:create snipt`
- `dokku postgres:create snipt`
- `dokku postgres:link snipt snipt`
- `scp snipt.dump nsergeant@server.nicksergeant.com:/home/nsergeant`
- `dokku postgres:connect snipt < snipt.dump`
- `dokku domains:add snipt snipt.net`
- `dokku storage:mount snipt /var/lib/dokku/data/storage/snipt-whoosh:/app/snipt-whoosh`
- `dokku config:set DOKKU_LETSENCRYPT_EMAIL=support@snipt.net SECRET_KEY=<some-secret-key> USE_SSL=true WHOOSH_PATH=/app/snipt-whoosh/whoosh_index`
- `git remote add dokku dokku@server.nicksergeant.com:snipt`
- `git push dokku`

## Automatic deploy to Heroku

You can click the button below to automatically deploy Snipt to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nicksergeant/snipt)

## Manual deploy to Heroku

- Clone the repo.
- `heroku create`
- `heroku addons:add heroku-postgresql:hobby-dev`
- `heroku addons:add searchbox`
- `heroku config:add SECRET_KEY=<some-secret-key>`
- `git push heroku`
- `heroku run python manage.py migrate`
- `heroku run python manage.py createsuperuser`
- Visit yourapp.herokuapp.com and login with the user you just created.

## Updating your Heroku instance after an automatic deploy

- `git clone https://github.com/nicksergeant/snipt`
- `cd snipt`
- `git checkout heroku`
- `heroku git:remote -a <your-instance-name>`
- `git push heroku heroku:master`

## Options

If you want email support (for password resets, server errors, etc):

- `heroku addons:create postmark:10k`
- `heroku run addons:open postmark` -> use an email you control and confirm it
- `heroku config:add POSTMARK_EMAIL=<email_from_above>`

If you want to disable user-facing signup:

- `heroku config:set DISABLE_SIGNUP=true`

If you want to enable Django's DEBUG mode:

- `heroku config:add DEBUG=true`

If you want to enable SSL on a custom domain after you've configured your
Heroku SSL cert:

- `heroku config:add USE_SSL=true`
