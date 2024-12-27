from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.fastapi_users_routers import current_user, current_superuser
from core.config import settings
from core.models import User
from core.schemas.user import UserRead

router = APIRouter(prefix=settings.api.v1.messages, tags=['Messages'])


@router.get('/messages')
def get_user_messages(user: Annotated[User, Depends(current_user)]):
    return {
        'messages': ['Hello', 'How are you?', 'I am a simple user'],
        'user': UserRead.model_validate(user)
    }


@router.get('/su-messages')
def get_superuser_messages(user: Annotated[User, Depends(current_superuser)]):
    return {
        'messages': ['Hello', 'How are you?', 'I am a superuser'],
        'user': UserRead.model_validate(user)
    }
