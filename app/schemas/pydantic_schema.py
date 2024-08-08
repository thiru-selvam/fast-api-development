from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass
