#!/bin/bash
ACTION=$1

function stop_stack() {
    docker stop snipt-proxy > /dev/null
    docker stop snipt-app > /dev/null
    docker stop snipt-es > /dev/null
    docker stop snipt-pg > /dev/null
}

function start_stack() {
    docker start snipt-pg > /dev/null
    docker start snipt-es > /dev/null
    docker start snipt-app > /dev/null
    docker start snipt-proxy > /dev/null
}

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
    docker run -it --name snipt-app -d -e DB_USER=postgres -e DB_NAME=postgres -e DEBUG=false -v /etc/settings_local.py:/app/snipt/settings_local.py --net container:snipt-net snipt/snipt
    sleep 5
    docker restart snipt-proxy
    echo "done"
fi

if [ "$ACTION" = "restart" ]; then
    echo "restarting app"
    docker restart snipt-app
fi

if [ "$ACTION" = "restart-stack" ]; then
    echo "restarting stack"
    stop_stack
    start_stack
fi

if [ "$ACTION" = "backupdb" ]; then
    echo "backing up db"
    docker run --rm --net container:snipt-net --entrypoint pg_dump postgres:9.1 -h 127.0.0.1 -U postgres snipt
fi

if [ "$ACTION" = "psql" ]; then
    docker run it --rm --net container:snipt-net --entrypoint psql postgres:9.1 -h 127.0.0.1 -U postgres snipt
fi
