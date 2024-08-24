import json
from typing import List
from uuid import UUID
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from psycopg2.extras import RealDictCursor, register_uuid
from sqlalchemy.orm import Session
from ..sql_alchemy.models import Posts, Users
from ..sql_alchemy.database import engine, get_db
from ..schemas import pydantic_schema as py_schema
from ..utils import oauth2
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# registering in psycopg package that we are using UUID
register_uuid()


@router.get("/", response_model=List[py_schema.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user:UUID=Depends(oauth2.get_current_user)):
    ## fetch posts only for current user
    # posts_data = db.query(Posts).filter(Posts.user_uid==current_user.uid).all()
    posts_data = db.query(Posts).all()
    return posts_data


@router.get('/{uid}', response_model=py_schema.PostOut)
def get_post(uid: UUID, db: Session = Depends(get_db), current_user:UUID=Depends(oauth2.get_current_user)):
    post_data = db.query(Posts).get(uid)
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested ID was not found for fetching")
    ## fetch post only for current user
    # if post_data.user_uid != current_user.uid:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to fetch this detail")
    return post_data


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=py_schema.PostOut)
def create_posts(payload: py_schema.PostIn, db: Session = Depends(get_db), current_user:UUID=Depends(oauth2.get_current_user)):
    new_post = Posts(user_uid=current_user.uid, **payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{uid}', response_model=py_schema.PostOut)
def update_post(uid: UUID, payload: py_schema.PostIn, db: Session = Depends(get_db), current_user:UUID=Depends(oauth2.get_current_user)):
    upt_query = db.query(Posts).filter(Posts.uid == uid)
    upt_data = upt_query.first()
    if upt_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested ID  was not found for updating")
    if upt_data.user_uid != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to perform this operation")

    upt_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    return upt_data


@router.delete('/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uid: UUID, db: Session = Depends(get_db), current_user:UUID=Depends(oauth2.get_current_user)):
    del_query = db.query(Posts).filter(Posts.uid == uid)
    del_data = del_query.first()
    if del_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested ID was not found deleting")
    if del_data.user_uid != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to perform this operation")

    del_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"successfully post was deleted"}

