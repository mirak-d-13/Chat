from app.db.models.group import Group, GroupMembership
from app.schemas.group import GroupCreate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class GroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, group_create: GroupCreate):
        group = Group(name=group_create.name, creator_id=group_create.creator_id)
        self.db.add(group)
        await self.db.commit()
        await self.db.refresh(group)

        for user_id in group_create.member_ids:
            membership = GroupMembership(group_id=group.id, user_id=user_id)
            self.db.add(membership)

        await self.db.commit()
        return group

    async def get_group_by_id(self, group_id: int):
        query = select(Group).filter(Group.id == group_id)
        result = await self.db.execute(query)
        group = result.scalars().first()
        return group

    async def get_all_groups(self):
        query = select(Group)
        result = await self.db.execute(query)
        groups = result.scalars().all()
        return groups
