#!/bin/bash
ACTION=$1

if [ "$ACTION" = "syncdb" ]; then
    docker run -it --rm -e DB_USER=postgres -e DB_NAME=postgres --net container:snipt-net snipt/snipt python manage.py syncdb --noinput
fi

if [ "$ACTION" = "migrate" ]; then
    docker run -it --rm -e DB_USER=postgres -e DB_NAME=postgres --net container:snipt-net snipt/snipt python manage.py migrate --noinput
fi

if [ "$ACTION" = "collectstatic" ]; then
    docker run -it --rm -v $(pwd)/static:/app/snipt/static --net container:snipt-net snipt/snipt python manage.py collectstatic --noinput
fi

if [ "$ACTION" = "deploy" ]; then
    echo "pulling latest image"
    docker pull snipt/snipt
    echo "stopping app"
    docker kill snipt-app
    docker rm snipt-app
    echo "deploying new container"
    docker run -it --name snipt-app -d -e DB_USER=postgres -e DB_NAME=postgres -e DEBUG=false --net container:snipt-net snipt/snipt
    echo "done"
fi

if [ "$ACTION" = "backupdb" ]; then
    echo "backing up db"
    docker run --rm --net container:snipt-net --entrypoint pg_dump postgres:9.1 -h 127.0.0.1 -U postgres snipt
fi
