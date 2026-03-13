FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir psycopg2-binary Flask Flask-CORS
COPY . .
CMD ["python", "app.py"]
