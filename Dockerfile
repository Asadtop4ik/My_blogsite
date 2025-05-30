FROM python:3.11-slim
LABEL authors="Asus"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && apt-get clean

COPY . /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000


CMD ["gunicorn", "myblogsite.wsgi:application", "--bind", "0.0.0.0:8000"]
