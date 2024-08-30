from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from psycopg2.extras import register_uuid
from sqlalchemy.orm import Session

from ..schemas.pydantic_schema import Like
from ..sql_alchemy.database import get_db
from ..sql_alchemy.models import Likes, Posts
from ..utils.oauth2 import get_current_user

router = APIRouter(prefix='/like', tags=['likes'])
# registering in psycopg package that we are using UUID
register_uuid()


@router.post('/', status_code=status.HTTP_201_CREATED)
def like_post(like_data: Like, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    liked_post_exist = db.query(Posts).filter(Posts.uid == like_data.post_uid).first()
    if not liked_post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Requested liked post does not exist")

    like_query = db.query(Likes).filter(Likes.post_uid == like_data.post_uid, Likes.user_uid == current_user.uid)
    found_like = like_query.first()
    if like_data.like:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"you are already liked this post")
        db.add(Likes(user_uid=current_user.uid, post_uid=like_data.post_uid))
        db.commit()
        return {'message': 'Successfully added like'}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"requested post for like does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Successfully removed like'}
