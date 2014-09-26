#!/bin/bash
COMPONENTS=$*
if [ -z "$COMPONENTS" ]; then
    echo "Usage: $0 [components]"
    exit 1
fi

for CMP in $COMPONENTS; do
    if [ "$CMP" = "all" ]; then
        # start net container
        docker run -it -p 80:80 -p 443:443 --name snipt-net -d debian:jessie bash > /dev/null
        sleep 1
    fi
    if [ "$CMP" = "postgres" -o "$CMP" = "all" ]; then
        echo "starting postgres"
        docker run -it -d --name snipt-pg --net container:snipt-net postgres:9.1 > /dev/null
        # wait for PG to start
        sleep 5
        # create db
        docker run -it --rm --net container:snipt-net --entrypoint createdb postgres:9.1 -h 127.0.0.1 -U postgres -E UTF8 -O postgres snipt
    fi

    if [ "$CMP" = "elasticsearch" -o "$CMP" = "all" ]; then
        echo "starting elasticsearch"
        docker run -it -d --name snipt-es --net container:snipt-net arcus/elasticsearch > /dev/null
        sleep 1
    fi
    
    if [ "$CMP" = "app" -o "$CMP" = "all" ]; then
        echo "starting app"
        # migrate
        docker run -it --rm -e DB_USER=postgres -e DB_NAME=snipt --net container:snipt-net snipt/snipt python manage.py syncdb --noinput
        docker run -it --rm -e DB_USER=postgres -e DB_NAME=snipt --net container:snipt-net snipt/snipt python manage.py migrate --noinput
        # collect static
        docker run -it --rm -v $(pwd)/static:/app/snipt/static --net container:snipt-net snipt/snipt python manage.py collectstatic --noinput
        # run app
        docker run -it --name snipt-app -d -e DB_USER=postgres -e DB_NAME=snipt -e DEBUG=false -v /etc/settings_local.py:/app/snipt/settings_local.py --net container:snipt-net snipt/snipt > /dev/null
        sleep 1
    fi

    if [ "$CMP" = "proxy" -o "$CMP" = "all" ]; then
        echo "starting proxy"
        docker run -d --name snipt-proxy -it -v /var/log/snipt:/logs -v $(pwd)/.docker/nginx.conf:/etc/nginx/nginx.conf -v $(pwd)/static:/app/snipt/static -v /etc/certs:/etc/certs --net container:snipt-net nginx nginx -g 'daemon off;' -c /etc/nginx/nginx.conf > /dev/null
    fi

done
