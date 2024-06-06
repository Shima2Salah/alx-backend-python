#!/usr/bin/env python3
'''second task'''
from typing import List, Union, Tuple, Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''concat func'''
    return lambda multiplier: multiplier * multiplier
