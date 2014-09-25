#!/bin/bash
APP_ROOT=/app
APP_DIR=$APP_ROOT/snipt
COOKIE_DOMAIN=${SESSION_COOKIE_DOMAIN:-.snipt.net}
SECRET_KEY=${SECRET_KEY:-changeme}
cp $APP_DIR/settings_local-template.py $APP_DIR/settings_local.py
# replace SESSION_COOKIE_DOMAIN
sed -i "s/^SESSION_COOKIE_DOMAIN.*/SESSION_COOKIE_DOMAIN = '$COOKIE_DOMAIN'/g" $APP_DIR/settings_local.py
sed -i "s/^SECRET_KEY.*/SECRET_KEY = '$SECRET_KEY'/g" $APP_DIR/settings_local.py
pushd $APP_DIR
python manage.py syncdb --noinput
python manage.py migrate --noinput
popd

pushd $APP_DIR
python manage.py run_gunicorn -c $APP_DIR/gunicorn.conf.server.py
