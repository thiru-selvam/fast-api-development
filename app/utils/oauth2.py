from fastapi import Depends, HTTPException, status
from jwt import PyJWT, PyJWTError
from uuid import UUID
from psycopg2.extras import register_uuid

from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.testing.suite.test_reflection import users

from ..schemas.pydantic_schema import TokenData
from ..sql_alchemy.database import get_db
from ..sql_alchemy.models import Users

# registering in psycopg package that we are using UUID
register_uuid()

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "d92003a7c5623d8df0c5d52b690102ef4201454bb3c37e9127eb42c28bf7166d"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 ##minutes

def generate_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = PyJWT().encode(key=SECRET_KEY, algorithm=ALGORITHM, payload=to_encode)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = PyJWT().decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        uid: UUID = payload.get('user_id')
        if not uid:
            raise credentials_exception
        token_data = TokenData(uid=uid)
    except PyJWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'credentials are invalid', headers={"WWW-Authenticate":"Bearer"})
    token =  verify_access_token(token, credentials_exception)
    user_data = db.query(Users).filter(Users.uid==token.uid).first()
    return user_data