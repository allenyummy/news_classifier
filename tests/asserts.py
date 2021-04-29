# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Utils for tests functions

import logging
from typing import List

logger = logging.getLogger(__name__)


def assert_ListOfListOfString(a: List[List[str]]):
    if not isinstance(a, list):
        return False
    for e in a:
        if not isinstance(e, list):
            return False
        for e_str in e:
            if not isinstance(e_str, str):
                return False
    return True


def assert_ExactSameLists(a: List[List[str]], b: List[List[str]]):
    if len(a) != len(b):
        return False
    for ea, eb in zip(a, b):
        if len(ea) != len(eb) or ea != eb:
            return False
    return True