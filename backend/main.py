from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Todo as TodoModel
from database import Base
from fastapi import Depends

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    id: int
    text: str
    completed: bool = False
    

class CreateTodo(BaseModel):
    text: str
    completed: bool = False


@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db:Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo

@app.post("/todos")
def create_todo(todo: CreateTodo, db:Session = Depends(get_db)):

    new_todo = TodoModel(
        text=todo.text,
        completed=todo.completed
)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: CreateTodo, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.text = updated_todo.text
    todo.completed = updated_todo.completed

    db.commit()
    db.refresh(todo)

    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int, db:Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return todo
