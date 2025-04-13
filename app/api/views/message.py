from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.message import MessageRepository
from app.db.models.db_helper import get_db_session
from app.schemas.message import MessageInDB

router = APIRouter()

@router.get("/history/{chat_id}", response_model=list[MessageInDB])
async def get_chat_history(chat_id: int, db: AsyncSession = Depends(get_db_session)):
    message_repo = MessageRepository(db)
    messages = await message_repo.get_messages_for_chat(chat_id)
    return messages