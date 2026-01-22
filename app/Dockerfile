FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir nicegui

COPY . /app 

CMD ["python", "/app/main.py"]
