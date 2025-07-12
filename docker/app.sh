#!/bin/bash
set -e


sleep 5

echo "=== Environment Debug ==="
echo "Все переменные:"
printenv | sort
echo "========================"


if [ -z "${DATABASE_URL}" ] && [ -z "${DB_HOST}" ]; then
  echo "FATAL: Ни DATABASE_URL, ни DB_* переменные не найдены!"
  echo "Проверьте настройки Environment в Render Dashboard"
  exit 1
fi


if [ -z "${DATABASE_URL}" ]; then
  export DATABASE_URL="postgresql+asyncpg://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}?ssl=require&timeout=30"
  echo "Собран DATABASE_URL из DB_* переменных"
fi

DECODED_URL=$(python3 -c "import urllib.parse; print(urllib.parse.unquote('${DATABASE_URL}'))")
PSQL_URL=$(echo "${DECODED_URL}" | sed 's/postgresql+asyncpg/postgresql/')

echo "Проверка подключения к PostgreSQL..."
for i in {1..30}; do
  if psql "${PSQL_URL}" -c "SELECT 1" >/dev/null 2>&1; then
    echo "Успешное подключение к PostgreSQL!"
    break
  fi
  echo "Попытка $i/30: Ожидание PostgreSQL..."
  sleep 2
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