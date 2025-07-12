#!/bin/bash


POSTGRES_HOST=$(echo "$DATABASE_URL" | sed -r 's/.*@([^:]+):.*/\1/')
while ! pg_isready -h "$POSTGRES_HOST" -p 5432; do
  echo "Waiting for PostgreSQL to start..."
  sleep 1
done


if ! alembic upgrade head; then
  echo "ALEMBIC MIGRATION FAILED!"
  exit 1
fi

# Запуск приложения через Gunicorn
exec gunicorn app.main:app \
  --workers 1\
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120

#while ! nc -z db 5432; do sleep 1; done
#
#
#
#alembic upgrade head
#
#gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#exec gunicorn app.main:app \
#    --workers 4 \
#    --worker-class uvicorn.workers.UvicornWorker \
#    --bind 0.0.0.0:8000