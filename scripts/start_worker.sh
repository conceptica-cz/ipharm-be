#!/bin/bash

./scripts/wait-for-it.sh $REDIS_HOST:$REDIS_PORT
./scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT

: ${WORKER_CONCURRENCY:=4}
celery -A ipharm_web.celery worker -E --loglevel=info --concurrency=$WORKER_CONCURRENCY -n worker
