from fastapi import FastAPI

from app.sql_alchemy.database import engine
from .routers import user, post, auth, likes
from .sql_alchemy import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Development")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)


@app.get("/")
def home_page():
    """Home URL

    Returns:
        string: welcome message
    """
    return {"message": "Welcome to Python API development using FastAPI"}
