# Snipt

This is the codebase for the website, [Snipt.net](https://snipt.net/).

It's a relatively well-kept Django app, so you shouldn't have too many problems getting a local copy running.

**Note:** These instructions assume you already have [Git](http://git-scm.com/) and [Mercurial](http://mercurial.selenic.com/) installed.

If you need help, visit `#snipt` on irc.freenode.net.

# Running the Django app

1. Clone the repo.
2. Setup a virtualenv.
3. `pip install -r requirements.txt`
4. `pip install --index-url https://code.stripe.com --upgrade stripe`
5. Copy settings_local-template.py to settings_local.py and edit the settings.
6. `python manage.py syncdb`
7. `python manage.py migrate`
8. `python manage.py runserver`

Any problems / questions / bugs, [create an issue](https://github.com/nicksergeant/snipt/issues). Thanks! :)
