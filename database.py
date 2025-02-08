import sqlite3
from config import DB_PATH

def init_db():
    """Создает таблицу пользователей, если её нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            latitude REAL,
            longitude REAL,
            favorite_color TEXT
        )
    ''')
    conn.commit()
    conn.close()

def user_exists(user_id):
    """Проверяет, есть ли пользователь в базе"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_user(user_id, name, phone, latitude, longitude, favorite_color):
    """Добавляет нового пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, name, phone, latitude, longitude, favorite_color))
    conn.commit()
    conn.close()

def get_user(user_id):
    """Получает данные пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def delete_user(user_id):
    """Удаляет пользователя из базы"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
