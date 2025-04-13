from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.auth import get_current_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = get_current_user_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_id
