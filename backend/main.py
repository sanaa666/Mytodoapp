from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
todos = []
next_id = 1

class Todo(BaseModel):
    id: int
    text: str
    completed: bool = False
    

class CreateTodo(BaseModel):
    text: str
    completed: bool = False


@app.get("/todos")
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
          return todo  


    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos")
def create_todo(todo: CreateTodo):
    global next_id
    new_todo = Todo(
        id=next_id,
        text=todo.text,
        completed=todo.completed
)

    todos.append(new_todo)
    next_id += 1

    return new_todo

@app.patch("/todos/{todo_id}")
def complete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = not todo.completed

            return todo

    raise HTTPException(status_code=404, detail="Todo not found")
        
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")

   
   
