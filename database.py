import sqlite3

DB_PATH = "users.db"

def init_db():
    """Создает таблицу пользователей, если она не существует"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT NOT NULL,
            phone_number TEXT,
            favorite_color TEXT,
            language TEXT DEFAULT 'ru'
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, user_name, phone_number, favorite_color=None, language='ru'):
    """Добавляет нового пользователя в базу данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, user_name, phone_number, favorite_color, language) VALUES (?, ?, ?, ?, ?)',
                   (user_id, user_name, phone_number, favorite_color, language))
    conn.commit()
    conn.close()

def user_exists(user_id):
    """Проверяет, существует ли пользователь в базе данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def delete_user(user_id):
    """Удаляет пользователя из базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def update_user_color(user_id, favorite_color):
    """Обновляет любимый цвет пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET favorite_color = ? WHERE user_id = ?", (favorite_color, user_id))
    conn.commit()
    conn.close()

def update_user_language(user_id, language):
    """Обновляет язык пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
    conn.commit()
    conn.close()

def get_user_info(user_id):
    """Получает информацию о пользователе"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, phone_number, favorite_color FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_user_language(user_id):
    """Получает язык пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'ru'
