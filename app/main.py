from uuid import UUID
from fastapi import FastAPI, Response, status, Depends, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .sql_alchemy import models
from .sql_alchemy.models import Posts
from app.sql_alchemy.database import engine, get_db
from .schemas.pydantic_schema import PostBase, PostCreate

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


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Posts).all()
    return {"status": "success", "data": posts}


@app.get('/posts/{uid}')
def get_post(uid: UUID, resp: Response, db: Session = Depends(get_db)):
    post_data = db.query(Posts).filter(Posts.uid == uid).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post data with id {uid} was not found")
    return {"data": post_data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: PostCreate, db: Session = Depends(get_db)):
    new_post = Posts(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"new_post": new_post}


@app.delete('/posts/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uid: UUID, db: Session = Depends(get_db)):
    del_query = db.query(Posts).filter(Posts.uid == uid)
    if del_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found in database")
    del_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"succesfully post was deleted"}


@app.put('/posts/{uid}')
def update_post(uid: UUID, payload: PostCreate, db: Session = Depends(get_db)):
    del_query = db.query(Posts).filter(Posts.uid == uid)
    if del_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found")
    del_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": del_query.first()}
