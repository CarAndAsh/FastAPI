from typing import Generator, Self, Annotated

from fastapi import Request, Header


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
