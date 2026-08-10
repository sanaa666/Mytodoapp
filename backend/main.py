from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import database
import sqlite3

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://sanaa666.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateUser(BaseModel):
    username: str

class CreateTodo(BaseModel):
    text: str
    completed: bool = False


@app.get("/todos")
def get_todos(user_id: int):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, text, completed, user_id FROM todos WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()

    conn.close()

    return[
        {
            "id": row[0],
            "text": row[1],
            "completed": bool(row[2]),
            "user_id": row[3]
        }
        for row in rows
    ]

@app.get("/todos/")
def get_todo(todo_id: int, user_id:int):
   conn = sqlite3.connect("todos.db")
   cursor = conn.cursor()

   cursor.execute(
       """
       SELECT id, text, completed, user_id
       FROM todos
       WHERE id = ? AND user_id = ?
       """,
       (todo_id, user_id)
   )

   row = cursor.fetchone()

   conn.close()

   if row is None:
       raise HTTPException(status_code=404, detail="Todo not found")
   

   return{
        "id": row[0],
        "text": row[1],
        "completed": bool(row[2]),
        "user_id": row[3]

    }


@app.post("/todos")
def create_todo(todo: CreateTodo, user_id: int):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos (text, completed, user_id) VALUES (?, ?, ?)",
        (todo.text, int(todo.completed), user_id)
        
    )

    conn.commit()

    todo_id = cursor.lastrowid

    conn.close()

    return{
        "id": todo_id,
        "text": todo.text,
        "completed": todo.completed,
        "user_id": user_id
    }

@app.post("/users")
def create_user(user: CreateUser):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (user.username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return{
            "id": existing_user[0],
            "username": user.username
        }

    cursor.execute(
        "INSERT INTO users (username) VALUES (?)",
        (user.username,)
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return{
        "id": user_id,
        "username": user.username

    }


@app.patch("/todos")
def complete_todo(todo_id: int, user_id: int):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, text, completed
        FROM todos
        WHERE id = ? AND user_id = ?
        """,
        (todo_id, user_id)
    )
    
    row = cursor.fetchone()
    
       
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    new_status = 0 if row[2] else 1


    cursor.execute(
        "UPDATE todos SET completed = ? WHERE id = ? AND user_id = ?",

        (new_status, todo_id, user_id)
    )

    conn.commit()
    conn.close()

    return{
        "id": row[0],
        "text": row[1],
        "completed": bool(row[new_status]),
        "user_id": user_id

    }

@app.put("/todos")
def edit_todo(todo_id:int, user_id:int, todo:CreateTodo):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, text, completed
        FROM todos
        WHERE id =? AND user_id = ?
        """,
        (todo_id, user_id)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    cursor.execute(
        """
        UPDATE todos
        SET text = ?, completed = ?
        WHERE id = ? AND user_id = ?
        """,
        (todo.text, int(todo.completed), todo_id, user_id)
    )

    conn.commit()
    conn.close()

    return{
        "id": todo_id,
        "text": todo.text,
        "completed": todo.completed,
        "user_id": user_id
    }
        
@app.delete("/todos")
def delete_todo(todo_id:int, user_id: int):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, text, completed
        FROM todos
        WHERE id = ? AND user_id = ?
        """,
        (todo_id, user_id)
    )
    
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    cursor.execute(
        "DELETE FROM todos WHERE id = ? AND user_id = ?",
        (todo_id, user_id)
    )
 
    conn.commit()
    conn.close()

    return{
        "id": row[0],
        "text": row[1],
        "completed": bool(row[2])
    
    }

   
   
