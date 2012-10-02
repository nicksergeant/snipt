# Snipt

This is the codebase for the website, [Snipt.net](https://snipt.net/).

It's a relatively well-kept Django app, so you shouldn't have too many problems
getting a local copy running.

# Running the Django app

1. Clone the repo.
2. Setup a virtualenv.
3. `pip install -r requirements.txt`
4. Copy local_settings-template.py to local_settings.py and edit the settings.
5. Comment out [this line](https://github.com/nicksergeant/snipt/blob/master/snipts/models.py#L19) from `snipts/models.py`
6. `python manage.py syncdb`
7. `python manage.py migrate`
8. Uncomment the line in `snipt/models.py`
9. `python manage.py runserver`

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
