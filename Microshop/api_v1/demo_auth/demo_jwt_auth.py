from fastapi import APIRouter, Depends, Form, HTTPException, status

from pydantic import BaseModel

from auth import utils as auth_utils
from users.schemas import UserSchema


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix='/jwt', tags=['JWT'])

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


@router.post('/login', response_model=TokenInfo)
def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email
    }
    token = auth_utils.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type='Bearer')
