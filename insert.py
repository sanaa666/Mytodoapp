import psycopg2
from backend.config import load_config

def insert_todo(todo_name, user_id):

    sql = """
            INSERT INTO todos (todo_name, todo_completed, user_id)
            VALUES(%s, %s, %s) RETURNING todo_id;"""

    todo_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (todo_name, 0, user_id))

                rows = cur.fetchone()
                if rows:
                    todo_id = rows[0]

                conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    return todo_id

if __name__== '__main__':
    target_user_id = 1
    inserted_id = insert_todo("cook rice", target_user_id)