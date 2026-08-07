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




class CreateTodo(BaseModel):
    text: str
    completed: bool = False


@app.get("/todos")
def get_todos():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    conn.close()

    return[
        {
            "id": row[0],
            "text": row[1],
            "completed": bool(row[2])
        }
        for row in rows
]

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
   conn = sqlite3.connect("todos.db")
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))

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
def create_todo(todo: CreateTodo):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos (text, completed) VALUES (?, ?)",
        (todo.text, int(todo.completed))
    )

    conn.commit()

    todo_id = cursor.lastrowid

    conn.close()

    return{
        "id": todo_id,
        "text": todo.text,
        "completed": todo.completed

    }


@app.patch("/todos/{todo_id}")
def complete_todo(todo_id: int):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
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
def delete_todo(todo_id:int):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
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

   
   
