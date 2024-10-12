FROM python:latest AS builder

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

FROM python:alpine

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000"]