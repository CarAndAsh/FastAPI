from typing import Annotated

from fastapi import APIRouter, Depends, Header

from utils.helper import GreatHelper, GreatService
from .dependencies_for_example.cls_deps import PathReaderDependency, path_reader
from .dependencies_for_example.func_deps import get_x_header, get_header_dependency, get_great_helper
from core.config import settings

router = APIRouter(tags=['Dependencies examples'], prefix=settings.api.v1.deps)


@router.get('/single-direct-dependency')
def single_direct_dependency(some_line: Annotated[str, Header()]):
    return {
        'text': some_line,
        'message': 'single direct depenpency some text',
    }


@router.get('/via-func-dependency')
def via_func_dependency(some_line: Annotated[str, Depends(get_x_header)]):
    return {
        'text': some_line,
        'message': 'single via func depenpency some text',
    }


@router.get('/single-dependencies')
def single_dependencies(
        some_first_line: Annotated[str, Header(alias='some_header')],
        some_second_line: Annotated[str, Depends(get_x_header)]
):
    return {
        'header 1': some_first_line,
        'header 2': some_second_line,
        'message': 'single via func depenpency some text',
    }


@router.get('/multi-indirect-dependency')
def multi_indirect_dependency(
        text_1: Annotated[str, Depends(get_header_dependency('header_1'))],
        text_2: Annotated[str, Depends(get_header_dependency('header_2', 'Hello, it is me'))]
):
    return {
        'header 1': text_1,
        'header 2': text_2,
        'message': 'multi-indirect dependency in use'
    }


@router.get('/top-level-helper-creation')
def top_level_helper_creation(
        helper_name: Annotated[str, Depends(get_header_dependency('helper_name', 'HelperOne'))],
        helper_default: Annotated[str, Depends(get_header_dependency('helper_default'))]
):
    helper = GreatHelper(name=helper_name, default=helper_default)
    return {
        'helper': helper.as_dict(),
        'message': 'top level helper creation'
    }


@router.get('/helper-as-dependency')
def helper_as_dependency(helper: Annotated[GreatHelper, Depends(get_great_helper)]):
    return {
        'helper': helper.as_dict(),
        'message': 'helper as dependency'
    }


@router.get('/great-service-as-dependency')
def great_service_as_dependency(service: Annotated[GreatService, Depends(GreatService)]):
    return {
        'service': service.as_dict(),
        'message': 'helper as dependency'
    }


@router.get('/path-reader-dependency-from-method')
def path_reader_dependency(
        reader: Annotated[
            PathReaderDependency,
            Depends(
                path_reader.as_dependency
                # or PathReaderDependency(source).as_dependency
            )
        ]
):
    return {
        'reader': reader.read(example='Hello world!'),
        'message': 'path reader dependency from method'
    }
