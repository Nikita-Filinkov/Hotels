FROM python:3.12


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /booking


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install alembic


COPY . .


RUN chmod a+x app.sh && \
    chmod a+x docker/*.sh


CMD ["./app.sh"]