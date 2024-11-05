from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError

from pydantic import BaseModel

from api_v1.demo_auth.helpers import create_access_token, create_refresh_token, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE
from auth import utils as auth_utils
from users.schemas import UserSchema


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/jwt', tags=['JWT'], dependencies=[Depends(http_bearer)])

oauth2_scheme = OAuth2PasswordBearer('api/v1/jwt/login/')

max = UserSchema(username='max', password=auth_utils.hash_password('pass'), email='max@examp.le')
zack = UserSchema(username='zack', password=auth_utils.hash_password('word'))
user_db: dict[str, UserSchema] = {
    max.username: max,
    zack.username: zack
}


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unath_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid login and password',
    )
    if not (user := user_db.get(username)):
        raise unath_exc
    if not auth_utils.check_password(password, user.password):
        raise unath_exc
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user inactive')
    return user


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'invalid token error: {exc}')
    return payload


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token type {token_type!r}, expected {ACCESS_TOKEN_TYPE!r}',
        )
    username: str | None = payload.get('sub')
    if user := user_db.get(username):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token invalid (user not found)')


def get_current_auth_active_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user inactive')


@router.post('/login/', response_model=TokenInfo)
def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='Bearer'
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
