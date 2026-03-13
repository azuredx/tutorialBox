import psycopg2
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "mydb"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "mypassword"),
    "port": "5432"
}

def init_database():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Создаём таблицу с новым полем age
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Проверяем, есть ли уже поле age (если таблица существовала)
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='age';
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE users ADD COLUMN age INTEGER;")
            print("Добавлено поле age в существующую таблицу")
        
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        
        if count == 0:
            cur.execute("""
                INSERT INTO users (name, email, age) VALUES 
                ('Иван Петров', 'ivan@example.com', 25),
                ('Мария Сидорова', 'maria@example.com', 30),
                ('Алексей Иванов', 'alex@example.com', 28);
            """)
            print("Добавлены тестовые пользователи с возрастом")
        
        conn.commit()
        cur.close()
        conn.close()
        print("База данных успешно обновлена!")
        
    except psycopg2.Error as e:
        print(f"Ошибка при инициализации БД: {e}")

if __name__ == "__main__":
    init_database()
