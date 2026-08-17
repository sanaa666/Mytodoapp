from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import traceback
from config import load_config
import sqlite3
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "http://localhost:8000",
                   "https://sanaa666.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateUser(BaseModel):
    username: str

class CreateTodo(BaseModel):
    text: str
    completed: int

def get_db_connection():
    config = load_config()
    return psycopg2.connect(**config)


@app.get("/todos")
def get_todos(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT todo_id, todo_name, todo_completed, user_id FROM todos WHERE user_id = %s ORDER BY todo_id ASC;",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return[
        {
            "id": row[0],
            "text": row[1],
            "completed": row[2],
            "user_id": row[3]
        }
        for row in rows
    ]

@app.get("/todos/")
def get_todo(todo_id: int, user_id:int):
   conn = get_db_connection()
   cur = conn.cursor()

   cur.execute(
       """
       SELECT todo_id, todo_name, todo_completed, user_id
       FROM todos
       WHERE todo_id = %s AND user_id = %s;
       """,
       (todo_id, user_id)
   )

   row = cur.fetchone()

   cur.close()
   conn.close()

   if row is None:
       raise HTTPException(status_code=404, detail="Todo not found")
   

   return{
        "id": row[0],
        "text": row[1],
        "completed": row[2],
        "user_id": row[3]

    }


@app.post("/todos")
def create_todo(todo: CreateTodo, user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO todos (todo_name, todo_completed, user_id)
            VALUES (%s, %s, %s)
            RETURNING todo_id;
            """,
            (todo.text, todo.completed, user_id)
            
        )

        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="failed to insert")

        todo_id = row[0]
        conn.commit()

        return{
            "id": todo_id,
            "text": todo.text,
            "completed": todo.completed,
            "user_id": user_id
        }

    except Exception as e:
        conn.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()

@app.post("/users")
def create_user(user: CreateUser):

    username = user.username.strip()
    
    if username == "":
        raise HTTPException(status_code=404, detail="Blank username.")
    
    conn = get_db_connection()
    cur = conn.cursor()

   
    cur.execute(
        "SELECT user_id FROM users WHERE user_name = %s",
        (username,)
    )
   

    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return{
            "id": existing_user[0],
            "username": username
        }

    cur.execute(
        "INSERT INTO users (user_name) VALUES (%s) RETURNING user_id;",
        (username,)
    )

    user_id = cur.fetchone()[0]
    conn.commit()


    cur.close()
    conn.close()

    return{
        "id": user_id,
        "username": username

    }


@app.patch("/todos")
def complete_todo(todo_id: int, user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT todo_id, todo_name, todo_completed
        FROM todos
        WHERE todo_id = %s AND user_id = %s
        """,
        (todo_id, user_id)
    )
    
    row = cur.fetchone()
    
       
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    new_status = 0 if row[2] else 1


    cur.execute(
        "UPDATE todos SET todo_completed = %s WHERE todo_id = %s AND user_id = %s",

        (new_status, todo_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return{
        "id": row[0],
        "text": row[1],
        "completed": int(new_status),
        "user_id": user_id

    }

@app.put("/todos")
def edit_todo(todo_id:int, user_id:int, todo:CreateTodo):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT todo_id, todo_name, todo_completed
        FROM todos
        WHERE todo_id =%s AND user_id = %s
        """,
        (todo_id, user_id)
    )

    row = cur.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    cur.execute(
        """
        UPDATE todos
        SET todo_name = %s, todo_completed = %s
        WHERE todo_id = %s AND user_id = %s
        """,
        (todo.text, int(todo.completed), todo_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return{
        "id": todo_id,
        "text": todo.text,
        "completed": todo.completed,
        "user_id": user_id
    }
        
@app.delete("/todos")
def delete_todo(todo_id:int, user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT todo_id, todo_name, todo_completed
        FROM todos
        WHERE todo_id = %s AND user_id = %s
        """,
        (todo_id, user_id)
    )
    
    row = cur.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    cur.execute(
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
        (todo_id, user_id)
    )
 
    conn.commit()
    cur.close()
    conn.close()

    return{
        "id": row[0],
        "text": row[1],
        "completed": row[2],
        "user_id": row[3]
    
    }

@app.delete("/users")
def delete_user(user_id:int):
    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "DELETE FROM users WHERE user_id = %s;",
            (user_id,)
        )
 
        conn.commit()
    finally:
        cur.close()
        conn.close()


   
   
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR.parent / "portal" / "dist"

app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

@app.get("/")
def serve_frontend():
    return FileResponse(DIST_DIR / "index.html")