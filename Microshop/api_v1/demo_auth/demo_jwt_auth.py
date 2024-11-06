from fastapi import (
    APIRouter, Depends
)
from fastapi.security import HTTPBearer

from pydantic import BaseModel

from api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token
)
from api_v1.demo_auth.validation import (
    get_current_token_payload,
    get_current_auth_user_for_refresh,
    get_current_auth_active_user, validate_auth_user
)
from users.schemas import UserSchema


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/jwt', tags=['JWT'], dependencies=[Depends(http_bearer)])


@router.post('/login/', response_model=TokenInfo)
def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='Bearer'
    )


@router.post('/refresh/', response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
        user: UserSchema = Depends(get_current_auth_user_for_refresh),
        # user: UserSchema = UserGetterFromToken(REFRESH_TOKEN_TYPE),
        # user: UserSchema = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get('/users/me/')
def auth_user_self_check_info(
        user: UserSchema = Depends(get_current_auth_active_user),
        payload: dict = Depends(get_current_token_payload)
):
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': payload.get('iat')
    }
