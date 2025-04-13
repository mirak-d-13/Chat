from fastapi import APIRouter, HTTPException, Depends
from app.schemas.chat import ChatCreate, ChatInDB
from app.db.repositories.chat import ChatRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.db_helper import get_db_session

router = APIRouter()


@router.post("/chats/", response_model=ChatInDB)
async def create_chat(
    chat_create: ChatCreate, db: AsyncSession = Depends(get_db_session)
):
    chat_repo = ChatRepository(db)
    new_chat = await chat_repo.create_chat(chat_create)
    return new_chat


@router.get("/chats/{chat_id}", response_model=ChatInDB)
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db_session)):
    chat_repo = ChatRepository(db)
    chat = await chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
