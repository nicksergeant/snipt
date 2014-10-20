# Snipt

This is the codebase for the website, [Snipt.net](https://snipt.net/).

# Running the Django app

1. Clone the repo.
2. Setup a virtualenv.
3. `pip install -r requirements.txt`
4. `pip install --index-url https://code.stripe.com --upgrade stripe`
5. `python manage.py syncdb`
6. `python manage.py migrate`
7. `python manage.py runserver`
8. If you created a superuser in the syncdb step, you need to also run `python manage.py backfill_api_keys` to generate an API key for that user.

# Deploying to Heroku

1. Clone the repo.
2. `heroku create`
3. `heroku config:add DEBUG=True`
3. `heroku config:add INTERCOM_SECRET_KEY=`
3. `heroku config:add POSTMARK_API_KEY=`
3. `heroku config:add RAVEN_CONFIG_DSN=`
3. `heroku config:add SECRET_KEY=`
3. `heroku config:add STRIPE_SECRET_KEY=`
4. `git push heroku`
5. `heroku run pip install --index-url https://code.stripe.com --upgrade stripe`
6. `heroku run python manage.py syncdb`
7. `heroku run python manage.py migrate`

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
