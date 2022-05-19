#!/bin/bash

./scripts/wait-for-it.sh $REDIS_HOST:$REDIS_PORT
./scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT



: ${WORKER_CONCURRENCY:=4}

QUEUS=high_priority,low_priority
NAME=worker

while getopts 'Q:n:' c
do
    case $c in
        Q) QUEUS=$OPTARG ;;
        n) NAME=$OPTARG ;;
    esac
done

celery -A ipharm_web.celery worker -E -Q $QUEUS --loglevel=info --concurrency=$WORKER_CONCURRENCY -n $NAME
