from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


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

    class Config:
        from_attributes = True


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email_id: EmailStr
    username: str


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    uid: UUID
    created_on: datetime

    class Config:
        from_attributes = True
