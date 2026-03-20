import sqlite3
import os 
from config import DB_FILE, DATA_FOLDER

def get_connection():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL,
        color TEXT NOT NULL,
        game TEXT NOT NULL,
        country TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(name) = LOWER(?)", (name,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(name, age, color, game, country):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, age, color, game, country)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, color, game, country))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def update_user(user_id, name=None, age=None, color=None, game=None, country=None):
    existing = get_user_by_id(user_id)
    if not existing:
        return False
    
    new_name = name if name is not None else existing["name"]
    new_age = age if age is not None else existing["age"]
    new_color = color if color is not None else existing["color"]
    new_game = game if game is not None else existing["game"]
    new_country = country if country is not None else existing["country"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET name = ?, age = ?, color = ?, game = ?, country = ?
        WHERE id = ?
    """, (new_name, new_age, new_color, new_game, new_country, user_id))
    conn.commit()
    conn.close()
    return True

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0

def get_filtered_users(country=None, game=None, page=1, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users"
    conditions = []
    params = []

    if country:
        conditions.append("LOWER(country) = LOWER(?)")
        params.append(country)
    
    if game:
        conditions.append("LOWER(game) = LOWER(?)")
        params.append(game)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY id LIMIT ? OFFSET ?"
    params.extend([limit, (page - 1) * limit])

    cursor.execute(query,tuple(params))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_total_users_count(country=None, game=None):
    conn = get_connection()
    cursor = conn.cursor()

    query ="SELECT COUNT(*) FROM users"
    conditions = []
    params = []

    if country:
        conditions.append("LOWER(country) = LOWER(?)")
        params.append(country)
    
    if game:
        conditions.append("LOWER(game) = LOWER(?)")
        params.append(game)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    cursor.execute(query, tuple(params))
    total = cursor.fetchone()[0]

    conn.close()
    return total