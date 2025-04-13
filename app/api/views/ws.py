from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.message import MessageRepository

from app.websockets.connection_manager import manager
from sqlalchemy.future import select
from app.db.models import Message
from app.db.models.group import GroupMembership

from app.core.auth import get_current_user_from_token
from app.db.models.db_helper import get_db_session

router = APIRouter()


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db_session),
):
    await manager.connect(user.id, websocket)

    last_message = None

    try:
        while True:
            data = await websocket.receive_text()

            query = (
                select(Message)
                .filter(Message.chat_id == chat_id)
                .order_by(Message.timestamp.desc())
                .limit(1)
            )
            result = await db.execute(query)
            last_message = result.scalars().first()

            if last_message and last_message.text == data:
                continue

            message_repo = MessageRepository(db)
            new_message = await message_repo.create_message(chat_id, user.id, data)

            group_query = select(GroupMembership).filter(
                GroupMembership.group_id == chat_id
            )
            group_result = await db.execute(group_query)
            group_members = group_result.scalars().all()

            for member in group_members:
                await manager.send_message_to_user(
                    member.user_id, f"[{user.name}]: {data}"
                )

            await manager.broadcast(f"[{user.name}]: {data}")

            await message_repo.mark_message_as_read(new_message.id)

    except Exception as e:
        manager.disconnect(user.id, websocket)
