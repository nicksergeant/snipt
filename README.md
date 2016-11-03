# Snipt

# Deploying to Heroku

**Automatic:**

You can click the button below to automatically deploy Snipt to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nicksergeant/snipt/tree/heroku)

**Please note:** this method will work fine, but you will not have email support
unless you manually configure Postmark. You don't necessarily need this,
though.  After deploying the instance, visit
`https://<your-instance-name>/signup`, and create a user. You will get a 500
Server Error, which is the site trying to send a welcome email. Ignore the
error and go to `<https://your-instance-name>/login`, and log in with the
username and password you provided. Snipt will work fine, but you will not
receive any emails if there are server errors.

If you would like to configure your instance to use a free Postmark addon, do
the following after deploying:

- `git clone https://github.com/nicksergeant/snipt.git`
- `cd snipt`
- `heroku git:remote -a <your-instance-name>`
- `heroku addons:open postmark` -> use an email you control and confirm it
- `heroku config:add POSTMARK_EMAIL=<email_from_above>`

**Manual:**

- Clone the repo.
- `heroku create`
- `heroku addons:add heroku-postgresql:hobby-dev`
- `heroku addons:add searchbox`
- `heroku addons:create postmark:10k`
- `heroku addons:open postmark` -> use an email you control and confirm it
- `heroku config:add POSTMARK_EMAIL=<email_from_above>`
- `heroku config:add SECRET_KEY=`
- `git push heroku`
- `heroku run python manage.py migrate`
- `heroku run python manage.py createsuperuser`
- Visit yourapp.herokuapp.com and login with the user you just created.

If you want to disable user-facing signup:

- `heroku config:set DISABLE_SIGNUP=true`

If you want to enable Disqus comments:

- `heroku config:set DISQUS_SHORTNAME=whatever`

If you want to enable Django's DEBUG mode:

- `heroku config:add DEBUG=False`

If you want to enable SSL (after you've configured your Heroku SSL cert):

- `heroku config:add USE_SSL=False`
