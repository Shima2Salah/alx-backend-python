#!/usr/bin/env python3
'''second task'''
from typing import Sequence, Any, Union, TypeVar, Mapping, Optional


T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default:
                     Union[T, None]) -> Union[Any, T]:
    '''safely get value func'''
    if key in dct:
        return dct[key]
    else:
        return default
