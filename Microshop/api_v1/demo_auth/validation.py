from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api_v1.demo_auth.crud import user_db
from api_v1.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth import utils as auth_utils
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer('api/v1/jwt/login/')


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'invalid token error: {exc}')
    return payload


def validate_token_type(payload: dict, token_type: str):
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token type {current_token_type!r}, expected {token_type!r}',
        )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get('sub')
    if user := user_db.get(username):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token invalid (user not found)')


# decompose variant 1 - func in func
def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


# decompose variant 2 - class
class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: dict = Depends(get_current_token_payload)):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_auth_active_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user inactive')


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
