from fastapi import FastAPI

from app.sql_alchemy.database import engine
from .routers import user, auth
from .sql_alchemy import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Known-Diff Automation Backend Development")

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def home_page():
    """Home URL

    Returns:
        string: welcome message
    """
    return {"message": "Welcome to Python Known-Diff Automation Backend Development"}
