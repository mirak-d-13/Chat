from app.db.models import Message
from app.schemas.message import MessageCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, message_create: MessageCreate):
        message = Message(
            chat_id=message_create.chat_id,
            sender_id=message_create.sender_id,
            text=message_create.text,
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages_by_chat_id(
        self, chat_id: int, limit: int = 10, offset: int = 0
    ):
        query = (
            select(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.timestamp)
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(query)
        messages = result.scalars().all()
        return messages
