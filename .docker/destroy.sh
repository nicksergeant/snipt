#!/bin/bash
COMPONENTS=$*
if [ -z "$COMPONENTS" ]; then
    echo "Usage: $0 [components]"
    exit 1
fi
for CMP in $COMPONENTS; do
    if [ "$CMP" = "postgres" -o "$CMP" = "all" ]; then
        echo "destroying postgres"
        docker kill snipt-pg
        docker rm snipt-pg
    fi
    if [ "$CMP" = "elasticsearch" -o "$CMP" = "all" ]; then
        echo "destroying elasticsearch"
        docker kill snipt-es
        docker rm snipt-es
    fi
    
    if [ "$CMP" = "app" -o "$CMP" = "all" ]; then
        echo "destroying app"
        docker kill snipt-app
        docker rm snipt-app
    fi

    if [ "$CMP" = "proxy" -o "$CMP" = "all" ]; then
        echo "destroying proxy"
        docker kill snipt-proxy
        docker rm snipt-proxy
    fi
    if [ "$CMP" = "all" ]; then
        docker kill snipt-net
        docker rm snipt-net
    fi
done
