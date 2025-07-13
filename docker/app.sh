#!/bin/bash
set -e

sleep 5



DB_URL=$(echo $DATABASE_URL | sed 's/postgresql+asyncpg/postgresql/g' | cut -d '?' -f 1)


echo "Проверка подключения к PostgreSQL..."
until pg_isready -d "$DB_URL"; do
    sleep 1
done


echo "Применение миграций Alembic..."
alembic upgrade head


echo "Проверка таблицы users..."
psql $DATABASE_URL -c "\dt" | grep users || {
    echo "Ошибка: таблица users не найдена!"
    exit 1
}

exec gunicorn app.main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
#exec gunicorn app.main:app \
#    --workers 4 \
#    --worker-class uvicorn.workers.UvicornWorker \
#    --bind 0.0.0.0:8000