#!/bin/bash
set -e

MAX_RETRIES=30
RETRY_DELAY=2

# Проверка DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
  echo "Ошибка: DATABASE_URL не установлена!"
  exit 1
fi


POSTGRES_HOST=$(echo "$DATABASE_URL" | sed -r 's/.*@([^/]+).*/\1/')

POSTGRES_HOST=$(echo "$POSTGRES_HOST" | cut -d: -f1)

echo "Ожидание доступности PostgreSQL на $POSTGRES_HOST (с SSL)..."

for i in $(seq 1 $MAX_RETRIES); do
  if psql "$DATABASE_URL" -c "SELECT 1" >/dev/null 2>&1; then
    echo "PostgreSQL доступен!"
    break
  fi
  echo "Попытка $i/$MAX_RETRIES: PostgreSQL не отвечает, ждем $RETRY_DELAY сек..."
  sleep $RETRY_DELAY

  if [ $i -eq $MAX_RETRIES ]; then
    echo "Ошибка: PostgreSQL не доступен после $MAX_RETRIES попыток!"
    echo "Проверьте:"
    echo "1. Правильность DATABASE_URL"
    echo "2. Доступность базы из сети (возможно, нужно добавить ваш IP в белый список)"
    echo "3. SSL параметры"
    exit 1
  fi
done

echo "Применение миграций Alembic..."
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