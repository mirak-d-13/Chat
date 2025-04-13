from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Message
from datetime import datetime


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, chat_id: int, sender_id: int, text: str) -> Message:
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text,
            timestamp=datetime.utcnow(),
            is_read=False
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_last_message_in_chat(self, chat_id: int) -> Message | None:
        result = await self.db.execute(
            select(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def mark_message_as_read(self, message_id: int):
        result = await self.db.execute(select(Message).filter(Message.id == message_id))
        message = result.scalars().first()
        if message and not message.is_read:
            message.is_read = True
            await self.db.commit()
            await self.db.refresh(message)
        return message

    async def get_messages_for_chat(self, chat_id: int, limit: int = 100) -> Message | list:
        result = await self.db.execute(
            select(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
            .limit(limit)
        )
        return result.scalars().all()