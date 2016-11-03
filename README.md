# Snipt

# Deploying to Heroku

*Automatic:*

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nicksergeant/snipt/tree/heroku)

*Manual:*

- Clone the repo.
- `heroku create`
- `heroku addons:add heroku-postgresql:hobby-dev`
- `heroku addons:add searchbox`
- `heroku addons:create postmark:10k`
- `heroku addons:open postmark` -> use an email you control
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
