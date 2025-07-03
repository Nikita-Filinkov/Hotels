#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=app.tasks.celery_connection:celery worker -l INFO --uid=nobody --gid=nogroup
elif [[ "${1}" == "flower" ]]; then
  celery --app=app.tasks.celery_connection:celery flower --address=0.0.0.0 --port=5555
fi


