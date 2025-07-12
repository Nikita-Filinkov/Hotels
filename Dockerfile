FROM python:3.12


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /booking

ENV DATABASE_URL=postgresql+asyncpg://nikita:3J8GLDKG0hGNDAmCHDN02yXMDIFT%3ARzw@dpg-dInv77c9e44c73er59dg-a.frankfurt-postgres.render.com/booking_db_84nx?ssl=require&timeout=30


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install alembic


COPY . .

RUN chmod +x docker/app.sh


CMD ["./docker/app.sh"]