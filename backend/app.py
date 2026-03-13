from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "mydb"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "mypassword"),
    "port": "5432"
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend is running"})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, age, created_at FROM users ORDER BY id;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users)
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    age = data.get('age', None)
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        if age:
            cur.execute(
                "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) RETURNING id;",
                (data['name'], data['email'], age)
            )
        else:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
                (data['name'], data['email'])
            )
        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": user_id, "message": "User created"}), 201
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
