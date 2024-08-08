from pydantic import BaseModel


class Posts(BaseModel):
    title: str
    content: str
    is_published: bool = True
    # rating: Optional[int] = None

