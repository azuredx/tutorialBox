import os
import signal
import sys
import logging
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])

# --- Configuration ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "mydb"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "mypassword"),
    "port": os.getenv("DB_PORT", "5432")
}

def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Поля: name, email, age (как ждет фронт)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Database init failed: {e}")

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None

# --- Graceful Shutdown ---
def handle_sigterm(*args):
    logger.info("Received SIGTERM. Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

# --- Routes ---

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Добавили /api/
@app.route('/api/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "ok", "db": "connected"}), 200
    return jsonify({"status": "error", "db": "disconnected"}), 503

# Добавили /api/
@app.route('/api/users', methods=['GET'])
@REQUEST_LATENCY.labels(endpoint='/api/users').time()
def get_users():
    conn = get_db_connection()
    if not conn:
        REQUEST_COUNT.labels(method='GET', endpoint='/api/users', http_status='500').inc()
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, age, created_at FROM users ORDER BY id;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        REQUEST_COUNT.labels(method='GET', endpoint='/api/users', http_status='200').inc()
        return jsonify(users)
    except psycopg2.Error as e:
        REQUEST_COUNT.labels(method='GET', endpoint='/api/users', http_status='500').inc()
        return jsonify({"error": str(e)}), 500

# Добавили /api/
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB error"}), 500
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) RETURNING id;",
            (data['name'], data['email'], data.get('age'))
        )
        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        REQUEST_COUNT.labels(method='POST', endpoint='/api/users', http_status='201').inc()
        return jsonify({"id": user_id, "message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "TutorialBox API v2.1 is running!"

if __name__ == '__main__':
    init_db() # Важно вызвать инициализацию!
    app.run(host='0.0.0.0', port=5000, debug=False)
