from typing import Generator, Self, Annotated

from fastapi import (Request, Header, HTTPException, status)
from pydantic import BaseModel


class PathReaderDependency:
    def __init__(self, source: str):
        self.source = source
        self._request: Request | None = None
        self._description: str = ''

    def as_dependency(
            self, request: Request,
            description: Annotated[str, Header(alias='x-description')]
    ) -> Generator[Self, None, None]:
        self._request = request
        self._description = description
        yield self
        self._request = None
        self._description = ''

    @property
    def path(self) -> str:
        if self._request:
            return self._request.url.path
        return ''

    def read(self, **kwargs: str) -> dict[str, str]:
        return {
            'source': self.source,
            'path': self.path,
            'description': self._description,
            'kwargs': kwargs
        }


path_reader = PathReaderDependency(source='home/usr/share')


class TokenData(BaseModel):
    # some data for example
    id: int
    username: str
    email: str


class TokenIntrospectResult(BaseModel):
    result: TokenData


class HeaderAccessDependency:
    def __init__(self, secret_token: str):
        self.secret_token = secret_token

    def validate(self, token: str) -> TokenIntrospectResult:
        if token != self.secret_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token is invalid'
            )
        # example of data
        return TokenIntrospectResult(result=TokenData(id=12, username='Neo', email='anderson@example.com'))

    def __call__(self, token: Annotated[str, Header(alias='x-access-token')]) -> TokenIntrospectResult:
        token_data = self.validate(token)
        # some logs
        return token_data


access_required = HeaderAccessDependency(secret_token='how-deep-is-the-rabbit-hole')
