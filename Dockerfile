
FROM python:3.10-alpine

LABEL authors="jerry george"

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .


VOLUME /app/instance

# Expose the port
EXPOSE 5000


CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
