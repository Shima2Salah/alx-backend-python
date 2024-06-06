#!/usr/bin/env python3
'''second task'''
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''safe first element func'''
    if lst:
        return lst[0]
    else:
        return None
