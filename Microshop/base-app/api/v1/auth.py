from fastapi import APIRouter

from api.dependencies.authentication.backend import authentication_backend
from api.v1.fastapi_users_routers import fastapi_users
from core.config import settings
from core.schemas.user import UserRead, UserCreate

router = APIRouter(prefix=settings.api.v1.auth, tags=['Auth'])
# /login and /logout
router.include_router(fastapi_users.get_auth_router(authentication_backend))
# /register
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))