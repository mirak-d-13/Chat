from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    name: str
    type: str


class ChatCreate(ChatBase):
    pass


class ChatInDB(ChatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
