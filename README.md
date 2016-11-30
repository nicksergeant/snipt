# Snipt

## Automatic deploy to Heroku

You can click the button below to automatically deploy Snipt to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nicksergeant/snipt)

#### Importing your snipts from Snipt.net

If you would like to import your snipts from Snipt.net before the service
closes on December 31st, 2016, follow these steps:

1. Deploy your own instance of Snipt using the "Deploy to Heroku" button
   above.
2. Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and set it up.
3. `git clone https://github.com/nicksergeant/snipt`
4. `cd snipt`
5. `heroku git:remote -a <your-heroku-app-name>`
6. `heroku run python manage.py createsuperuser`
7. Get your [Snipt.net API key](https://snipt.net/api/).
8. `heroku run python manage.py import_snipts <snipt.net-api-key> <snipt.net-username> <your-instance-superuser-username>`

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

- `heroku config:add DEBUG=False`

If you want to enable SSL on a custom domain after you've configured your
Heroku SSL cert:

- `heroku config:add USE_SSL=False`
