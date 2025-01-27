# Use a lightweight Python image
FROM python:3.10-alpine

LABEL authors="jerry george"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app/instance

EXPOSE 5000

CMD ["python", "app.py"]
