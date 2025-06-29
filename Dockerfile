FROM python:3.12-alpine

RUN apk --no-cache add --virtual build-dependencies \
    gcc \
    musl-dev \
    libffi-dev \
    libressl-dev \
    libxml2-dev \
    libxslt-dev \
    py3-pip \
 && pip install --no-cache-dir scrapyd python-dotenv psycopg2-binary \
 && apk del build-dependencies \
 && apk add \
    libressl \
    libxml2 \
    libxslt

# Создаём необходимые каталоги
RUN mkdir -p /src/eggs/myproject

# Копируем конфигурацию и .egg
COPY ./scrapyd.conf /etc/scrapyd/
COPY myproject.egg /src/eggs/myproject/1.egg

EXPOSE 6800

VOLUME ["/etc/scrapyd/", "/var/lib/scrapyd/"]

ENTRYPOINT ["scrapyd", "--pidfile="]