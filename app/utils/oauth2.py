from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWT, PyJWTError
from psycopg2.extras import register_uuid
from sqlalchemy.orm import Session

from ..config import settings
from ..schemas.pydantic_schema import TokenData
from ..sql_alchemy.database import get_db
from ..sql_alchemy.models import Users

# registering in psycopg package that we are using UUID
register_uuid()

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  ##minutes


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = PyJWT().encode(key=SECRET_KEY, algorithm=ALGORITHM, payload=to_encode)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = PyJWT().decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        uid: UUID = payload.get('user_id')
        if not uid:
            raise credentials_exception
        token_data = TokenData(uid=uid)
    except PyJWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'credentials are invalid',
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user_data = db.query(Users).filter(Users.uid == token.uid).first()
    return user_data
