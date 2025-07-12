#!/bin/bash
set -e


echo "=== Проверка окружения ==="
echo "DATABASE_URL: ${DATABASE_URL:0:30}..."  # Выводим часть URL для проверки
echo "DB_HOST: $DB_HOST"

MAX_RETRIES=30
RETRY_DELAY=2


if [ -z "$DATABASE_URL" ] && [ -z "$DB_HOST" ]; then
  echo "ОШИБКА: Не найдены переменные подключения к БД!"
  echo "Должна быть указана либо DATABASE_URL, либо набор DB_* переменных"
  exit 1
fi


if [ -z "$DATABASE_URL" ]; then
  export DATABASE_URL="postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME?ssl=require"
  echo "Собран DATABASE_URL из DB_* переменных"
fi


DECODED_DB_URL=$(printf '%b' "${DATABASE_URL//%/\\x}")


PSQL_URL=$(echo "$DECODED_DB_URL" | sed 's/postgresql+asyncpg/postgresql/g')

echo "Ожидание доступности PostgreSQL (host: ${DB_HOST:-$POSTGRES_HOST})..."

for i in $(seq 1 $MAX_RETRIES); do
  if psql "$PSQL_URL" -c "SELECT 1" >/dev/null 2>&1; then
    echo "PostgreSQL доступен!"
    break
  fi
  echo "Попытка $i/$MAX_RETRIES: PostgreSQL не отвечает, ждем $RETRY_DELAY сек..."
  sleep $RETRY_DELAY

  if [ $i -eq $MAX_RETRIES ]; then
    echo "ОШИБКА: Не удалось подключиться к PostgreSQL!"
    echo "Проверьте:"
    echo "1. Доступность БД в панели Render"
    echo "2. Whitelist IP (должен быть 0.0.0.0/0)"
    echo "3. Правильность учётных данных"
    echo "4. Попробуйте подключиться вручную:"
    echo "   psql \"$PSQL_URL\" -c \"SELECT 1\""
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