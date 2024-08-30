from uuid import UUID

from fastapi import status, Depends, HTTPException, APIRouter
from psycopg2.extras import register_uuid
from sqlalchemy.orm import Session

from ..schemas import pydantic_schema as py_schema
from ..sql_alchemy.database import get_db
from ..sql_alchemy.models import Users
from ..utils.hashing_ import hash_pass

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# registering in psycopg package that we are using UUID
register_uuid()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=py_schema.UserOut)
def create_user(payload: py_schema.UserIn, db: Session = Depends(get_db)):
    # hash the user password
    hashed_pass = hash_pass(payload.password)
    payload.password = hashed_pass
    # payload.full_name = f"{payload.first_name} {payload.last_name}"
    user_data = Users(**payload.model_dump())
    try:
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This email is already registered')


@router.get('/{uid}', status_code=status.HTTP_200_OK, response_model=py_schema.UserOut)
def get_user(uid: UUID, db: Session = Depends(get_db)):
    users_data = db.query(Users).get(uid)
    if not users_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"requested ID was not found for fetching")
    return users_data
