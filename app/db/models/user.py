from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    messages = relationship("Message", back_populates="sender")
    groups = relationship("GroupMembership", back_populates="user")
