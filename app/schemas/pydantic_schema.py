from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email_id: EmailStr


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    uid: UUID
    created_on: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email_id: EmailStr
    password: str


class TokenData(BaseModel):
    uid: Optional[UUID] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class BasePost(BaseModel):
    title: str
    content: str
    is_published: bool = True
    # rating: Optional[int] = None


class PostIn(BasePost):
    pass


class PostOut(BasePost):
    uid: UUID
    created_on: datetime
    user_uid: UUID
    user_info: UserOut

    class Config:
        from_attributes = True

class PostLikes(PostOut):
    likes:int

class Like(BaseModel):
    post_uid: UUID
    like: bool
