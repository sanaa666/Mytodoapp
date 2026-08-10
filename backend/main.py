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
def get_todos(username: str):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    if user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    

    user_id = user[0]
    print("USERNAME:", username)
    print("USER ID:, user_id")
    cursor.execute("SELECT id, username FROM users")
    print("USERS:", cursor.fetchall())
 
    cursor.execute("SELECT id, text, user_id FROM todos")
    print("ALL TODOS:", cursor.fetchall())
    
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

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, username:str):
   conn = sqlite3.connect("todos.db")
   cursor = conn.cursor()

   cursor.execute(
       """
       SELECT todos.id, todos.text, todos.completed
       FROM todos
       JOIN users ON todos.user_id = users.id
       WHERE todos.id = ? AND users.username = ?
       """,
       (todo_id, username)
   )

   row = cursor.fetchone()

   conn.close()

   if row is None:
       raise HTTPException(status_code=404, detail="Todo not found")
   

   return{
        "id": row[0],
        "text": row[1],
        "completed": bool(row[2])

    }


@app.post("/todos")
def create_todo(todo: CreateTodo, username: str):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    if user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = user[0]

    cursor.execute(
        "INSERT INTO todos (text, completed, user_id) VALUES (?, ?, ?)",
        (todo.text, int(todo.completed), user_id,)
        
    )

    conn.commit()

    todo_id = cursor.lastrowid

    conn.close()

    return{
        "id": todo_id,
        "text": todo.text,
        "completed": todo.completed

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


@app.patch("/todos/{todo_id}")
def complete_todo(todo_id: int, username: str):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT todos.id, todos.text, todos.completed
        FROM todos
        JOIN users ON todos.user_id = users.id
        WHERE todos.id = ? AND users.username = ?
        """,
        (todo_id, username)
    )
    
    row = cursor.fetchone()
    
       
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    new_status = 0 if row[2] else 1


    cursor.execute(
        "UPDATE todos SET completed = ? WHERE id = ?",

        (new_status, todo_id)
    )

    conn.commit()
    conn.close()

    return{
        "id": row[0],
        "text": row[1],
        "completed": bool(row[2])

    }

        
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int, username: str):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT todos.id, todos.text, todos.completed
        FROM todos
        JOIN users ON todos.user_id = users.id
        WHERE todos.id = ? AND users.username = ?
        """,
        (todo_id, username)
    )
    
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    cursor.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )
 
    conn.commit()
    conn.close()

    return{
        "id": row[0],
        "text": row[1],
        "completed": bool(row[2])
    
    }

   
   
