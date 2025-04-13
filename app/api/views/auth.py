from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate
from app.db.repositories.user import UserRepository
from app.core.auth import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.db.models.db_helper import get_db_session

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token")
async def login_for_access_token(
    user_create: UserCreate, db: AsyncSession = Depends(get_db_session)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(user_create.email)

    if user is None or not pwd_context.verify(
        user_create.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
