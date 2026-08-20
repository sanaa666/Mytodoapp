from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import traceback
from config import load_config
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import bcrypt
import os
import secrets
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv

ALGORITHM = "HS256"

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Secret key env variable missing")

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "portal" / "dist" if (BASE_DIR / "portal" / "dist").exists() else BASE_DIR.parent / "portal" / "dist"

(DIST_DIR / "assets").mkdir(parents=True, exist_ok=True)

app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name = "assets")

@app.get("/")
def serve_frontend():
    return FileResponse(DIST_DIR / "index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "http://127.0.0.1:8000",
                   "http://localhost:8000",
                   "https://sanaa666.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCredentials(BaseModel):
    username: str
    password: str

class CreateTodo(BaseModel):
    text: str
    completed: int



def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)
    else:
        config = load_config()
        return psycopg2.connect(**config)

from create_tables import create_tables

@app.on_event("startup")
def startup_event():
    try:
        create_tables()
        print("tables created")
    except Exception as e:
        print(f"errorL {e}")


@app.get("/todos")
def get_todos(session_token: str = Cookie(None)):
    user_id = get_current_user_id(session_token)
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
            "completed": int(row[2]),
            "user_id": row[3]
        }
        for row in rows
    ]

@app.get("/todos/")
def get_todo(todo_id: int, session_token: str = Cookie(None)):

   user_id = get_current_user_id(session_token)
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
        "completed": int(row[2]),
        "user_id": row[3],

    }


@app.post("/todos")
def create_todo(todo: CreateTodo, session_token: str = Cookie(None)):
    user_id = get_current_user_id(session_token)
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO todos (todo_name, todo_completed, user_id)
            VALUES (%s, %s, %s)
            RETURNING todo_id;
            """,
            (todo.text, int(todo.completed), user_id)
            
        )

        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="failed to insert")

        todo_id = row[0]
        conn.commit()

        return{
            "id": todo_id,
            "text": todo.text,
            "completed": int(todo.completed),
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
def create_user(user: UserCredentials):

    username = user.username.strip()
    password = user.password.strip()
    
    if not username:
        raise HTTPException(status_code=400, detail="Blank username.")

    if not password:
        raise HTTPException(status_code=400, detail="Blank password.")

    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_bytes.decode('utf-8')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT user_id FROM users WHERE user_name = %s",
            (username,)
        )

        if cur.fetchone():
            raise HTTPException(status_code=409, detail="Username already exists")

    

        cur.execute(
            "INSERT INTO users (user_name, password_hash) VALUES (%s, %s) RETURNING user_id;",
            (username, hashed_password)
        )


        user_id = cur.fetchone()[0]
        conn.commit()

        return{
            "id": user_id,
            "username": username
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
    

@app.patch("/todos")
def complete_todo(todo_id: int, session_token: str = Cookie(None)):
    user_id = get_current_user_id(session_token)
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
        "user_id": user_id,

    }

@app.put("/todos")
def edit_todo(todo_id:int, todo:CreateTodo, session_token: str = Cookie(None)):
    user_id = get_current_user_id(session_token)

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
        "completed": int(todo.completed),
        "user_id": user_id
    }
        
@app.delete("/todos")
def delete_todo(todo_id:int, session_token: str = Cookie(None)):
    user_id = get_current_user_id(session_token)
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT todo_id, todo_name, todo_completed, user_id
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
        "completed": int(row[2]),
        "user_id": row[3]
    
    }

@app.delete("/users")
def delete_user(session_token: str = Cookie(None)):
    user_id = get_current_user_id(session_token)
    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "DELETE FROM users WHERE user_id = %s RETURNING user_id;",
            (user_id,)
        )
        deleted_user = cur.fetchone()

        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        
 
        conn.commit()
        response = JSONResponse(
            content={"detail": "user deleted succesfully"})
        
        response.delete_cookie(
            key="session_token",
            samesite="none",
            secure=True,
            httponly=True,
        )
        return response
    finally:
        cur.close()
        conn.close()

@app.post("/login")
def log_in(user: UserCredentials, response: Response):
    username = user.username.strip()
    password = user.password.strip()
        
    if not username:
        raise HTTPException(status_code=400, detail="Blank username.")
    
    if not password:
        raise HTTPException(status_code=400, detail="Blank password.")
        
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
            cur.execute(
                "SELECT user_id, password_hash FROM users WHERE user_name = %s",
                (username,),
            )

            row = cur.fetchone()

            if row is None:
                 raise HTTPException(status_code=401, detail="Invalid user or pass")

            user_id, stored_hash = row
            try:

                is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            except Exception:
                is_valid = False

            if not is_valid:
                raise HTTPException(status_code=401, detail="invalid user or pass")

            expiration = datetime.now(timezone.utc) + timedelta(hours=24)
            payload ={
                "user_id": user_id,
                "exp": expiration
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            response.set_cookie(
                key="session_token",
                value=token,
                httponly=True,
                samesite="none",
                secure=True
            )
        
            return{
                "id": user_id,
                "username": username
            }

    finally:
            cur.close()
            conn.close()

@app.post("/logout")
def logout(response:Response):
        response.delete_cookie(
            key="session_token",
            samesite="none",
            secure=True,
            httponly=True
        )
        return {"detail": "logged out successfully"}

def get_current_user_id(session_token: str=Cookie(None)) -> int:
    if session_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(session_token, SECRET_KEY, algorithms =[ALGORITHM])
        return payload["user_id"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")