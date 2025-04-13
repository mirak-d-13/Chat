from fastapi import APIRouter, Depends
from app.schemas.message import MessageCreate, MessageInDB
from app.db.repositories.message import MessageRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.db_helper import get_db_session


router = APIRouter()


@router.post("/messages/", response_model=MessageInDB)
async def create_message(
    message_create: MessageCreate, db: AsyncSession = Depends(get_db_session)
):
    message_repo = MessageRepository(db)
    new_message = await message_repo.create_message(message_create)
    return new_message


@router.get("/messages/{chat_id}", response_model=list[MessageInDB])
async def get_messages(
    chat_id: int,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session),
):
    message_repo = MessageRepository(db)
    messages = await message_repo.get_messages_by_chat_id(chat_id, limit, offset)
    return messages
