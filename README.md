# Snipt

This is the codebase for the website, [Snipt.net](https://snipt.net/).

It's a relatively well-kept Django app, so you shouldn't have too many problems getting a local copy running.

These instructions assume you already have [Git](http://git-scm.com/) and [Mercurial](http://mercurial.selenic.com/) installed via your OS package manager or from source.

If you need help, visit `#snipt` on irc.freenode.net.

# Running the Django app

1. Clone the repo.
2. Setup a virtualenv.
3. `pip install -r requirements.txt`
4. `pip install --index-url https://code.stripe.com --upgrade stripe`
5. Copy local_settings-template.py to local_settings.py and edit the settings.
6. Comment out [this line](https://github.com/nicksergeant/snipt/blob/master/snipts/models.py#L19) from `snipts/models.py`
7. `python manage.py syncdb`
8. `python manage.py migrate`
9. Uncomment the line in `snipt/models.py`
10. `python manage.py runserver`

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
