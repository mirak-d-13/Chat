from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.db_helper import get_db_session
from app.schemas.user import UserCreate, UserInDB, UserUpdate
from app.db.repositories.user import UserRepository
from app.core.auth import create_access_token
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users/", response_model=UserInDB)
async def create_user(
    user_create: UserCreate, db: AsyncSession = Depends(get_db_session)
):
    user_repo = UserRepository(db)

    existing_user = await user_repo.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = await user_repo.create_user(user_create)

    access_token = create_access_token(data={"sub": str(new_user.id)})

    return {"user": new_user, "access_token": access_token, "token_type": "bearer"}


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


@router.patch("/users/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    user_repo = UserRepository(db)
    updated_user = await user_repo.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
