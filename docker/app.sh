#!/bin/bash


# Извлекаем параметры подключения из DATABASE_URL
DB_HOST=$(echo $DATABASE_URL | awk -F'[@:]' '{print $4}')
DB_USER=$(echo $DATABASE_URL | awk -F'[:/@]' '{print $4}')
DB_NAME=$(echo $DATABASE_URL | awk -F'/' '{print $NF}')

# Ожидание доступности PostgreSQL
echo "Waiting for PostgreSQL at $DB_HOST..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Применение миграций с подробным логированием
echo "=== Current migrations status ==="
alembic current
echo "=== Applying migrations ==="
alembic upgrade head
if [ $? -ne 0 ]; then
  echo "!!! MIGRATION FAILED !!!"
  echo "Creating tables directly from models..."
  python -c "
import asyncio
from app.models import Base
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine('$DATABASE_URL')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(create_tables())
"
  if [ $? -ne 0 ]; then
    echo "!!! FAILED TO CREATE TABLES !!!"
    exit 1
  fi
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