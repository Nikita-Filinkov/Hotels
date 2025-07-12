#!/bin/bash
set -e

MAX_RETRIES=60
RETRY_DELAY=2

# Проверка DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
  echo "Ошибка: DATABASE_URL не установлена!"
  exit 1
fi


DECODED_DB_URL=$(printf '%b' "${DATABASE_URL//%/\\x}")


PSQL_URL=$(echo "$DECODED_DB_URL" | sed 's/postgresql+asyncpg/postgresql/g')

echo "Ожидание доступности PostgreSQL..."
for i in $(seq 1 $MAX_RETRIES); do
  if psql "$PSQL_URL" -c "SELECT 1" >/dev/null 2>&1; then
    echo "PostgreSQL доступен!"
    break
  fi
  echo "Попытка $i/$MAX_RETRIES: PostgreSQL не отвечает, ждем $RETRY_DELAY сек..."
  sleep $RETRY_DELAY

  if [ $i -eq $MAX_RETRIES ]; then
    echo "Ошибка: PostgreSQL не доступен после $MAX_RETRIES попыток!"
    echo "Проверьте:"
    echo "1. DATABASE_URL в настройках Render"
    echo "2. Доступность БД в панели Render"
    echo "3. WhiteList IP в настройках БД"
    exit 1
  fi
done

echo "Применение миграций..."
alembic upgrade head

echo "Запуск Gunicorn..."
exec gunicorn app.main:app \
  --workers 1 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -

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