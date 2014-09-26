#!/bin/bash
COMPONENTS=$*
if [ -z "$COMPONENTS" ]; then
    echo "Usage: $0 [components]"
    exit 1
fi

for CMP in $COMPONENTS; do
    if [ "$CMP" = "all" ]; then
        # start net container
        docker run -it -p 8000:80 --name snipt-net -d debian:jessie bash
        sleep 1
    fi
    if [ "$CMP" = "postgres" -o "$CMP" = "all" ]; then
        echo "starting postgres"
        docker run -it -d --name snipt-pg --net container:snipt-net postgres:9.1
        # wait for PG to start
        sleep 5
    fi

    if [ "$CMP" = "elasticsearch" -o "$CMP" = "all" ]; then
        echo "starting elasticsearch"
        docker run -it -d --name snipt-es --net container:snipt-net arcus/elasticsearch
        sleep 1
    fi
    
    if [ "$CMP" = "app" -o "$CMP" = "all" ]; then
        echo "starting app"
        # migrate
        docker run -it --rm -e DB_USER=postgres -e DB_NAME=postgres --net container:snipt-net snipt/snipt python manage.py syncdb --noinput
        docker run -it --rm -e DB_USER=postgres -e DB_NAME=postgres --net container:snipt-net snipt/snipt python manage.py migrate --noinput
        # collect static
        docker run -it --rm -v $(pwd)/static:/app/snipt/static --net container:snipt-net snipt/snipt python manage.py collectstatic --noinput
        # run app
        docker run -it --name snipt-app -d -e DB_USER=postgres -e DB_NAME=postgres -e DEBUG=false --net container:snipt-net snipt/snipt
        sleep 1
    fi

    if [ "$CMP" = "proxy" -o "$CMP" = "all" ]; then
        echo "starting proxy"
        docker run -d --name snipt-proxy -it -v $(pwd)/.docker/nginx.conf:/etc/nginx/nginx.conf -v $(pwd)/static:/app/snipt/static --net container:snipt-net nginx nginx -g 'daemon off;' -c /etc/nginx/nginx.conf
    fi

done
