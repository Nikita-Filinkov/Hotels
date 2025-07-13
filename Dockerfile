FROM python:3.12

RUN apt-get update && apt-get install -y postgresql-client netcat

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /booking

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt alembic

COPY . .

RUN chmod +x docker/app.sh

CMD ["./docker/app.sh"]