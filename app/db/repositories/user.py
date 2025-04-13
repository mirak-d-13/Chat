from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_create: UserCreate):
        hashed_password = pwd_context.hash(user_create.password)
        user = User(
            name=user_create.name,
            email=user_create.email,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int):
        query = select(User).filter(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        return user

    async def get_user_by_email(self, email: str):
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        user = result.scalars().first()
        return user

    async def update_user(self, user_id: int, user_update: UserUpdate):
        user = await self.get_user_by_id(user_id)
        if user:
            if user_update.name:
                user.name = user_update.name
            if user_update.email:
                user.email = user_update.email
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        return None

    async def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
