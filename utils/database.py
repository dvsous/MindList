import sqlite3

def connect_db():
    return sqlite3.connect("data.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        content TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


# Notes
def add_note(title, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()


def get_notes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM notes")
    rows = cursor.fetchall()
    conn.close()
    return {title: content for title, content in rows}


def delete_note(title):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE title = ?", (title,))
    conn.commit()
    conn.close()


# Tasks
def add_todo(text):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (text, done) VALUES (?, 0)", (text,))
    conn.commit()
    conn.close()


def get_todos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, done FROM todos")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "text": r[1], "done": bool(r[2])} for r in rows]


def update_todo_done(todo_id, done):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET done = ? WHERE id = ?", (1 if done else 0, todo_id))
    conn.commit()
    conn.close()


def delete_todo(todo_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()


def clear_todos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos")
    conn.commit()
    conn.close()