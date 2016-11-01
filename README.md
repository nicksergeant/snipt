# Snipt

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
