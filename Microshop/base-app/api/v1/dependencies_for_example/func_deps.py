from typing import Annotated

from fastapi import Header


def get_x_header(header: Annotated[str, Header(alias='x-header')] = '') -> str:
    return header


def get_header_dependency(header_name: str, default_value: str = ''):
    def dependency(header: Annotated[str, Header(alias=header_name)] = default_value) -> str:
        return header

    return dependency
