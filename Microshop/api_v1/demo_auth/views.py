import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix='/demo-auth', tags=['Demo Auth'])
security = HTTPBasic()


@router.get('/basic-auth/')
def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        'message': 'Good time!',
        'username': credentials.username,
        'password': credentials.password
    }


###################################### FOR EXAMPLE. ALL SAME DATA MUST BE IN DB. ######################################

username_to_password = {'admin': 'admin', 'user': 'user', 'gin': 'tonic'}
static_auth_token_to_username = {
    'ef8d678988863e39a48b72e4e2ac52b7': 'admin',
    'f51ca4db98f9e799f313b7da3ac9cc9c': 'gin'
}


#######################################################################################################################

def get_username_by_static_auth_token(static_token: str = Header(alias='x-auth-token')) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='invalid token')


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid login or password',
        headers={'WWW-Authenticate': 'Basic'},
    )
    correct_password = username_to_password.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    if not secrets.compare_digest(credentials.password.encode('utf-8'), correct_password.encode('utf-8')):
        raise unauthed_exc
    return credentials.username


@router.get('/basic-auth-username/')
def demo_basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {'message': f'Be happy {auth_username}!'}


@router.get('/some-http-header-auth/')
def demo_some_http_header_auth(username: str = Depends(get_username_by_static_auth_token)):
    return {'message': f'Nice to meet you {username}!'}
