#!/usr/bin/env python3
'''second task'''
from typing import List, Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''concat func'''
    return k, v * v
