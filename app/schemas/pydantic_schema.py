from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    designation: str
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


# class BaseKnownDiff(BaseModel):
#     diff_name: str
#     rule_id: str
#     diff_url: str
#     description: dict
#     raised_by: str
#     diff_image: str
#     assigned_to: str
#     is_active: bool = True
#     # rating: Optional[int] = None
#
#
# class PostIn(BaseKnownDiff):
#     pass
#
#
# class PostOut(BasePost):
#     uid: UUID
#     created_on: datetime
#     user_uid: UUID
#     user_info: UserOut
#
#     class Config:
#         from_attributes = True
#
# class PostLikes(PostOut):
#     likes:int
