#!/bin/bash
COMPONENTS=$*
if [ -z "$COMPONENTS" ]; then
    echo "Usage: $0 [components]"
    exit 1
fi
for CMP in $COMPONENTS; do
    if [ "$CMP" = "postgres" -o "$CMP" = "all" ]; then
        echo "destroying postgres"
        docker kill snipt-pg > /dev/null
        docker rm snipt-pg > /dev/null
    fi
    if [ "$CMP" = "elasticsearch" -o "$CMP" = "all" ]; then
        echo "destroying elasticsearch"
        docker kill snipt-es > /dev/null
        docker rm snipt-es > /dev/null
    fi
    
    if [ "$CMP" = "app" -o "$CMP" = "all" ]; then
        echo "destroying app"
        docker kill snipt-app > /dev/null
        docker rm snipt-app > /dev/null
    fi

    if [ "$CMP" = "proxy" -o "$CMP" = "all" ]; then
        echo "destroying proxy"
        docker kill snipt-proxy > /dev/null
        docker rm snipt-proxy > /dev/null
    fi
    if [ "$CMP" = "all" ]; then
        echo "destroying shared net"
        docker kill snipt-net > /dev/null
        docker rm snipt-net > /dev/null
    fi
done
