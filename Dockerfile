# Dockerfile

FROM python:3.11-slim

# Ishchi papkani aniqlash
WORKDIR /app

# Zarur paketlarni o‘rnatish
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc netcat-openbsd \
    && apt-get clean


# Fayllarni konteynerga ko‘chirish
COPY . /app

# entrypoint faylga ruxsat berish
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Python kutubxonalarni o‘rnatish
RUN pip install --upgrade pip && pip install -r requirements.txt

# Portni ochish
EXPOSE 8000

# Konteyner ishga tushganda bajariladigan komanda
ENTRYPOINT ["/entrypoint.sh"]
