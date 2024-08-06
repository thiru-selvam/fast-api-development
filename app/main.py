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


def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def home_page():
    """Home URL

    Returns:
        string: message hello world
    """
    return {"message": "Hello world"}


@app.get("/posts")
def get_all_posts():
    return {"data": my_posts}


@app.get('/posts/{uid}')
def get_post(uid: int, resp: Response):
    post_data = find_posts(uid)
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post data with id {uid} was not found")
    return {"data": post_data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Posts):
    post_dict = payload.model_dump()
    post_dict['id'] = randint(3, 100000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}


@app.delete('/posts/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uid: int):
    post_index = find_index_post(uid)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found in database")
    my_posts.pop(post_index)
    return {"message": f"succesfully post was deleted"}
    

@app.put('/posts/{uid}')
def update_post(uid: int, payload: Posts):
    print(payload)
    post_index = find_index_post(uid)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {uid} was not found")
    post_data = payload.model_dump()
    post_data['id'] = uid
    my_posts[post_index] = post_data
    return {"message": "Successfully post was updated"}
