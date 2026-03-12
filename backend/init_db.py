import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "port": "5432"
}

def init_database():
    """Создает таблицу users если её нет"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Создаем таблицу
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Добавим пару тестовых пользователей (если таблица пустая)
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        
        if count == 0:
            cur.execute("""
                INSERT INTO users (name, email) VALUES 
                ('Иван Петров', 'ivan@example.com'),
                ('Мария Сидорова', 'maria@example.com'),
                ('Алексей Иванов', 'alex@example.com');
            """)
            print("Добавлены тестовые пользователи")
        
        conn.commit()
        cur.close()
        conn.close()
        print("База данных успешно инициализирована!")
        
    except psycopg2.Error as e:
        print(f"Ошибка при инициализации БД: {e}")

if __name__ == "__main__":
    init_database()
