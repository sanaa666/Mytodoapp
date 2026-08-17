import psycopg2
from backend.config import load_config

def delete_todo(todo_id):
    rows_deleted = 0
    sql = 'DELETE FROM todos WHERE todo_id = %s'
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (todo_id,))
                rows_deleted = cur.rowcount

            conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    return rows_deleted

if __name__ == '__main__':
    deleted_rows = delete_todo(1)