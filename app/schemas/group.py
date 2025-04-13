from pydantic import BaseModel, ConfigDict



class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    creator_id: int
    member_ids: list[int]


class GroupInDB(GroupBase):
    id: int
    creator_id: int

    class Config:
        from_attributes = True


class GroupMembershipInDB(BaseModel):
    group_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
