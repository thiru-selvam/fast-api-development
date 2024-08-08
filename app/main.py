from random import randint
import sys
from uuid import UUID
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# registering in psycopg package that we are using UUID
psycopg2.extras.register_uuid()


class Posts(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None


# DataBase connection

def init_db_conn():
    try:
        db_conn = psycopg2.connect(database='fast_api_dev', host='127.0.0.1', port='5432', user='root',
                                   password='Selva@14599', cursor_factory=RealDictCursor)
        db_cursor = db_conn.cursor()
        print('Database connection successfull!!')
        return db_conn, db_cursor, None
    except Exception as e:
        return None, None, e


client_conn, client_cursor, err = init_db_conn()

# exit the program if db connection failed
if err is not None:
    raise RuntimeError("Failed to connect db", err)

my_posts = [{"id": 1, 'title': 'post 1', 'content': 'content 1', 'published': True, 'rating': 4},
            {"id": 2, 'title': 'post 2', 'content': 'content 2', 'published': True, 'rating': 2}]


def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def home_page():
    """Home URL

    Returns:
        string: message hello world
    """
    return {"message": "Hello world"}


@app.get("/posts")
def get_all_posts():
    client_cursor.execute(""" select  * from posts""")
    post_all_data = client_cursor.fetchall()
    client_conn.commit()
    return {"data": post_all_data}


@app.get('/posts/{uid}')
def get_post(uid: UUID, resp: Response):
    print(uid, type(uid))
    client_cursor.execute(""" select * from posts where uid = %s """, (uid,))
    single_post_data = client_cursor.fetchone()
    client_conn.commit()
    if not single_post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post data with id {uid} was not found")
    return {"data": single_post_data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Posts):
    client_cursor.execute(
        """INSERT INTO posts (post_title, post_content, is_published) VALUES (%s, %s, %s) RETURNING * """,
        (payload.title, payload.content, payload.published))
    created_post = client_cursor.fetchone()
    client_conn.commit()
    return {"new_post": created_post}


@app.delete('/posts/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uid: int):
    post_index = find_index_post(uid)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found in database")
    my_posts.pop(post_index)
    return {"message": f"succesfully post was deleted"}


@app.put('/posts/{uid}')
def update_post(uid: int, payload: Posts):
    print(payload)
    post_index = find_index_post(uid)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found")
    post_data = payload.model_dump()
    post_data['id'] = uid
    my_posts[post_index] = post_data
    return {"message": "Successfully post was updated"}
