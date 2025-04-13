from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    chat_id: int
    sender_id: int
    text: str


class MessageCreate(MessageBase):
    pass


class MessageInDB(MessageBase):
    id: int
    timestamp: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)
