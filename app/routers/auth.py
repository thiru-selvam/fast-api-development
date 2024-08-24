from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from ..sql_alchemy.database import get_db
from ..sql_alchemy.models import Users
from ..schemas.pydantic_schema import UserLogin, Token
from ..utils.hashing_ import verify_hash
from ..utils.oauth2 import generate_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=Token)
def login(user_credential:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    userdata = db.query(Users).filter(user_credential.username == Users.email_id).first()
    if not userdata:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials, User not found")
    if not verify_hash(user_credential.password, userdata.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials, password is incorrect")
    access_token  = generate_access_token(data={"user_id":str(userdata.uid)})
    return {'access_token': access_token, 'token_type':'bearer'}