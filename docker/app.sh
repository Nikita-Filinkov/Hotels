#!/bin/bash

# Извлекаем хост БД из DATABASE_URL
DB_HOST=$(echo $DATABASE_URL | awk -F'[@:]' '{print $4}')

# Ожидание доступности PostgreSQL
echo "Waiting for PostgreSQL at $DB_HOST..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Applying database migrations..."
alembic upgrade head
if [ $? -ne 0 ]; then
  echo "Failed to apply migrations!"
  exit 1
fi

# Запуск приложения
exec gunicorn app.main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000

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