import asyncio
from app.db.models.db_helper import db_helper
from app.db.repositories.user import UserRepository
from app.schemas.user import UserCreate


async def create_users():
    async with db_helper.session_factory() as session:
        user_repo = UserRepository(session)

        for i in range(5):
            user_create = UserCreate(
                name=f"User{i}",
                email=f"user{i}@example.com",
                password="test123"
            )
            await user_repo.create_user(user_create)

if __name__ == "__main__":
    asyncio.run(create_users())