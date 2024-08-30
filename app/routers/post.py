from typing import List, Optional
from uuid import UUID

from fastapi import status, Depends, HTTPException, APIRouter
from psycopg2.extras import register_uuid
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..schemas import pydantic_schema as py_schema
from ..sql_alchemy.database import get_db
from ..sql_alchemy.models import Posts, Likes
from ..utils import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# registering in psycopg package that we are using UUID
register_uuid()


@router.get("/", response_model=List[py_schema.PostLikes])
def get_all_posts(db: Session = Depends(get_db),
                  current_user: UUID = Depends(oauth2.get_current_user)):
    ##fetch all posts
    # posts_data = db.query(Posts).all()

    posts_data = (db
                  .query(Posts, func.count(Likes.post_uid).label('likes'))
                  .join(Likes, Posts.uid == Likes.post_uid, isouter=True)
                  .group_by(Posts.uid)
                  .all())

    posts_wit_likes = [setattr(post, 'likes', count) or post for post, count in posts_data]

    return posts_wit_likes


@router.get("/query", response_model=List[py_schema.PostLikes])
def get_all_posts(db: Session = Depends(get_db),
                  current_user: UUID = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    ## fetch posts only for current user
    # posts_data = db.query(Posts).filter(Posts.user_uid==current_user.uid).all()

    posts_data = (db
                  .query(Posts, func.count(Likes.post_uid).label('likes'))
                  .join(Likes, Posts.uid == Likes.post_uid, isouter=True)
                  .group_by(Posts.uid)
                  .filter(Posts.content.contains(search))
                  .limit(limit)
                  .offset(skip)
                  .all())
    posts_wit_likes = [setattr(post, 'likes', count) or post for post, count in posts_data]
    return posts_wit_likes


@router.get('/{uid}', response_model=py_schema.PostLikes)
def get_post(uid: UUID,
             db: Session = Depends(get_db),
             current_user: UUID = Depends(oauth2.get_current_user)):

    ## fetch post only for current user
    # if post_data.user_uid != current_user.uid:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to fetch this detail")

    post_data = (db
                 .query(Posts, func.count(Likes.post_uid).label('likes'))
                 .join(Likes, Posts.uid == Likes.post_uid, isouter=True)
                 .group_by(Posts.uid)
                 .filter(Posts.uid==uid)
                 .first())
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested ID was not found for fetching")
    post, count = post_data
    post.likes = count
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=py_schema.PostOut)
def create_posts(payload: py_schema.PostIn, db: Session = Depends(get_db),
                 current_user: UUID = Depends(oauth2.get_current_user)):
    new_post = Posts(user_uid=current_user.uid, **payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{uid}', response_model=py_schema.PostOut)
def update_post(uid: UUID, payload: py_schema.PostIn, db: Session = Depends(get_db),
                current_user: UUID = Depends(oauth2.get_current_user)):
    upt_query = db.query(Posts).filter(Posts.uid == uid)
    upt_data = upt_query.first()
    if upt_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested ID  was not found for updating")
    if upt_data.user_uid != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform this operation")

    upt_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    return upt_data


@router.delete('/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uid: UUID, db: Session = Depends(get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    del_query = db.query(Posts).filter(Posts.uid == uid)
    del_data = del_query.first()
    if del_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested ID was not found deleting")
    if del_data.user_uid != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform this operation")

    del_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"successfully post was deleted"}
