from fastapi import APIRouter, HTTPException, Depends
from app.schemas.group import GroupCreate, GroupInDB
from app.db.repositories.group import GroupRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.db_helper import get_db_session

router = APIRouter()


@router.post("/groups/", response_model=GroupInDB)
async def create_group(
    group_create: GroupCreate, db: AsyncSession = Depends(get_db_session)
):
    group_repo = GroupRepository(db)
    new_group = await group_repo.create_group(group_create)
    return new_group


@router.get("/groups/{group_id}", response_model=GroupInDB)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db_session)):
    group_repo = GroupRepository(db)
    group = await group_repo.get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.get("/groups/", response_model=list[GroupInDB])
async def get_all_groups(db: AsyncSession = Depends(get_db_session)):
    group_repo = GroupRepository(db)
    groups = await group_repo.get_all_groups()
    return groups
