import sqlite3

def init_db():
    conn = sqlite3.connect("todos.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()