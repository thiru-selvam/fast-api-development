from random import randint
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"id": 1, 'title': 'post 1', 'content': 'content 1', 'published': True, 'rating': 4},
            {"id": 2, 'title': 'post 2', 'content': 'content 2', 'published': True, 'rating': 2}]


@app.get("/")
def home_page():
    return {"message": "Hello world"}


@app.get("/posts")
def get_all_posts():
    return {"data": my_posts}


@app.get('/posts/{uid}')
def get_post(uid: int, resp: Response):
    post_data = [i for i in my_posts if i['id'] == uid]
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post data with 11id {uid} was not found")
        # resp.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"{uid} was not found"}
    return {"data": post_data}


@app.post("/posts")
def create_posts(payload: Posts):  # def create_posts(payload: dict = Body(...)):
    post_dict = payload.model_dump()  # print(payload.dict) {"title": payload.title, "content": payload.content}
    post_dict['id'] = randint(3, 100000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}
