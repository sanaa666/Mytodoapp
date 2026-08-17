import psycopg2
from backend.config import load_config

def update_todo(todo_id, todo_name):
    updated_row_count = 0

    sql = """UPDATE todos
                SET todo_name = %s
                WHERE todo_id = %s"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (todo_name, todo_id))
                updated_row_count = cur.rowcount

            conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return updated_row_count

if __name__ == '__main__':
    update_todo(1, "eat beetroot")