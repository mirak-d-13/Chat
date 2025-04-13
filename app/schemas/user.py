from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: str | None = None
    email: str | None = None


class UserInDB(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
