#!/bin/bash
set -e

sleep 5


if [ -z "$DATABASE_URL" ]; then
    echo "ОШИБКА: Переменная DATABASE_URL не установлена!"
    exit 1
fi


DB_HOST=$(echo $DATABASE_URL | awk -F[@] '{print $2}' | awk -F[/] '{print $1}' | awk -F[:] '{print $1}')
DB_PORT=$(echo $DATABASE_URL | awk -F[@] '{print $2}' | awk -F[/] '{print $1}' | awk -F[:] '{print $2}')
DB_NAME=$(echo $DATABASE_URL | awk -F[/] '{print $NF}' | awk -F[?] '{print $1}')
DB_USER=$(echo $DATABASE_URL | awk -F[/] '{print $3}' | awk -F[:] '{print $1}')
DB_PASS=$(echo $DATABASE_URL | awk -F[/] '{print $3}' | awk -F[:] '{print $2}' | awk -F[@] '{print $1}')


DB_PORT=${DB_PORT:-5432}


echo "Проверка подключения к PostgreSQL ($DB_HOST:$DB_PORT)..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
    echo "Ожидание PostgreSQL ($DB_HOST:$DB_PORT)..."
    sleep 2
done


echo "Применение миграций Alembic..."
alembic upgrade head


echo "Проверка таблицы users..."
if ! PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "\dt users" | grep -q "public.*users"; then
    echo "ОШИБКА: таблица users не найдена!"
    echo "Список всех таблиц в базе $DB_NAME:"
    PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "\dt"
    exit 1
fi


exec gunicorn app.main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
#exec gunicorn app.main:app \
#    --workers 4 \
#    --worker-class uvicorn.workers.UvicornWorker \
#    --bind 0.0.0.0:8000