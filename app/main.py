from fastapi import FastAPI
from app.api.views import user, chat, group, message, ws

app = FastAPI()
#
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(group.router, prefix="/group", tags=["group"])
app.include_router(message.router, prefix="/message", tags=["message"])
app.include_router(ws.router, prefix="/ws", tags=["ws"])