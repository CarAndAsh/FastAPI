from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserRead, UserCreate
from .crud.users import get_all_users, create_user

router = APIRouter(tags=['Users'])


@router.get('', response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await get_all_users(session=session)
    return users


@router.post('', response_model=UserRead)
async def add_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_create: UserCreate,
):
    user = await create_user(session=session, user_create=user_create)
    return user
