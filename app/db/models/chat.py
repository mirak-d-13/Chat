from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)  # "private" или "group"

    messages = relationship("Message", back_populates="chat")
