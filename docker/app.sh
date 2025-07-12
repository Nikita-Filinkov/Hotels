#!/bin/bash


MAX_RETRIES=30
RETRY_DELAY=2

POSTGRES_HOST=$(echo "$DATABASE_URL" | sed -r 's/.*@([^:]+):.*/\1/')

echo "Ожидание доступности PostgreSQL на $POSTGRES_HOST..."
for i in $(seq 1 $MAX_RETRIES); do
  if pg_isready -h "$POSTGRES_HOST" -p 5432 -q; then
    echo "PostgreSQL доступен!"
    break
  fi
  echo "Попытка $i/$MAX_RETRIES: PostgreSQL не отвечает, ждем $RETRY_DELAY сек..."
  sleep $RETRY_DELAY

  if [ $i -eq $MAX_RETRIES ]; then
    echo "Ошибка: PostgreSQL не стал доступен после $MAX_RETRIES попыток!"
    exit 1
  fi
done

echo "Применение миграций Alembic (с таймаутом 5 минут)..."
if ! timeout 300 alembic upgrade head; then
  echo "Ошибка: Миграции не применились за отведенное время!"
  exit 1
fi


echo "Запуск Gunicorn..."
exec gunicorn app.main:app \
  --workers 1 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --preload

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