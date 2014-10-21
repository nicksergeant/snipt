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
3. `heroku addons:add heroku-postgresql:standard-0`
4. `heroku addons:add bonsai`
5. `heroku config:add AWS_ACCESS_KEY_ID=`
6. `heroku config:add AWS_SECRET_ACCESS_KEY=`
7. `heroku config:add AWS_STORAGE_BUCKET_NAME=`
8. `heroku config:add DEBUG=False`
9. `heroku config:add INTERCOM_SECRET_KEY=`
10. `heroku config:add POSTMARK_API_KEY=`
11. `heroku config:add RAVEN_CONFIG_DSN=`
12. `heroku config:add SECRET_KEY=`
13. `heroku config:add STRIPE_SECRET_KEY=`
14. `heroku config:add USE_SSL=False`
15. `git push heroku`
16. `heroku run pip install --index-url https://code.stripe.com --upgrade stripe`
17. `heroku run python manage.py syncdb`
18. `heroku run python manage.py migrate`

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
