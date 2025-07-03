#!/bin/bash

while ! nc -z db 5432; do sleep 1; done



alembic upgrade head

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#exec gunicorn app.main:app \
#    --workers 4 \
#    --worker-class uvicorn.workers.UvicornWorker \
#    --bind 0.0.0.0:8000