from app.db.models import Chat
from app.schemas.chat import ChatCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self, chat_create: ChatCreate):
        chat = Chat(name=chat_create.name, type=chat_create.type)
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def get_chat_by_id(self, chat_id: int):
        query = select(Chat).filter(Chat.id == chat_id)
        result = await self.db.execute(query)
        chat = result.scalars().first()
        return chat
