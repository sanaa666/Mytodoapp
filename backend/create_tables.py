import psycopg2
import os
from config import load_config

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)
    else:
        config = load_config()
        return psycopg2.connect(**config)

def create_tables():
    commands = (
        """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    user_name VARCHAR(20) NOT NULL UNIQUE,
                    password_hash VARCHAR (255) NOT NULL
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS todos(
            todo_id SERIAL PRIMARY KEY,
            todo_name VARCHAR(255) NOT NULL,
            todo_completed INTEGER NOT NULL DEFAULT 0,
            user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
            
        );

        """)

    try:
        with get_connection() as conn:
              
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)

            conn.commit()
        print("tables created")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def default_user():
    sql = """
    INSERT INTO users(user_id, user_name, password_hash)
    VALUES (1, 'default_user', 'dummy_hash_or_actual_hashed_pass')
    ON CONFLICT (user_id) DO NOTHING;
    """

    try:
            config = load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                        cur.execute(sql)
    
                conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)

def default_todo():
    sql = """
    INSERT INTO todos(todo_id, todo_text, todo_completed, user_id)
    VALUES(1, 'clean room', 1,1)
    ON CONFLICT (todo_id) DO NOTHING;
    """
    try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                            cur.execute(sql)
        
                    conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
                print(error)


if __name__ == '__main__':
    create_tables()
    default_user()
        
  