from typing import Annotated

from fastapi import Header, Depends

from utils.helper import GreatHelper


def get_x_header(header: Annotated[str, Header(alias='x-header')] = '') -> str:
    return header


def get_header_dependency(header_name: str, default_value: str = ''):
    def dependency(header: Annotated[str, Header(alias=header_name)] = default_value) -> str:
        return header

    return dependency


def get_great_helper(
        helper_name: Annotated[str, Depends(get_header_dependency('helper_name'))],
        helper_default: Annotated[str, Depends(get_header_dependency('helper_default'))]
) -> GreatHelper:
    helper = GreatHelper(name=helper_name, default=helper_default)
    return helper
