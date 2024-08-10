from typing import List
from uuid import UUID
from fastapi import FastAPI, Response, status, Depends, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .sql_alchemy import models
from .sql_alchemy.models import Posts, Users
from app.sql_alchemy.database import engine, get_db
from .schemas import pydantic_schema as py_schema
from .utils.hashing_ import hash_pass

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# registering in psycopg package that we are using UUID
psycopg2.extras.register_uuid()


@app.get("/")
def home_page():
    """Home URL

    Returns:
        string: message hello world
    """
    return {"message": "Hello world"}


@app.get("/posts", response_model=List[py_schema.PostOut])
def get_all_posts(db: Session = Depends(get_db)):
    posts_data = db.query(Posts).all()
    return posts_data


@app.get('/posts/{uid}', response_model=py_schema.PostOut)
def get_post(uid: UUID, db: Session = Depends(get_db)):
    post_data = db.query(Posts).filter(Posts.uid == uid).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post data with id {uid} was not found")
    return post_data


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=py_schema.PostOut)
def create_posts(payload: py_schema.PostIn, db: Session = Depends(get_db)):
    new_post = Posts(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete('/posts/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uid: UUID, db: Session = Depends(get_db)):
    del_query = db.query(Posts).filter(Posts.uid == uid)
    if del_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found in database")
    del_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"successfully post was deleted"}


@app.put('/posts/{uid}', response_model=py_schema.PostOut)
def update_post(uid: UUID, payload: py_schema.PostIn, db: Session = Depends(get_db)):
    upt_query = db.query(Posts).filter(Posts.uid == uid)
    if upt_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found")
    upt_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    return {"updated_data": upt_query.first()}


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=py_schema.UserOut)
def create_user(payload: py_schema.UserIn, db: Session = Depends(get_db)):
    # hash the user password
    hashed_pass = hash_pass(payload.password)
    payload.password = hashed_pass
    user_data = Users(**payload.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data
