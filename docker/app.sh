#!/bin/bash

while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL to start..."
  sleep 1
done



alembic upgrade head
if [ $? -ne 0 ]; then
    echo "Migration failed! Exiting..."
    exit 1
fi

exec gunicorn app.main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
#exec gunicorn app.main:app \
#    --workers 4 \
#    --worker-class uvicorn.workers.UvicornWorker \
#    --bind 0.0.0.0:8000