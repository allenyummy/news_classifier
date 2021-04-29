# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Check type of input text and Transform

import logging
from typing import List, Union

logger = logging.getLogger(__name__)


def is_string(text):
    if isinstance(text, str):
        return True
    return False


def is_list_of_string(text):
    if isinstance(text, list) and all(isinstance(i, str) for i in text):
        return True
    return False


def is_nested_list_of_string(text):
    if isinstance(text, list):
        for i in text:
            if not isinstance(i, list):
                return False
            for j in i:
                if not isinstance(j, str):
                    return False
        return True
    return False


def check_input_type_and_transform(
    text: Union[str, List[str], List[List[str]]], is_split_into_words: bool
) -> Union[List[str], List[List[str]]]:

    if is_string(text):
        if is_split_into_words:
            raise ValueError("Type of the input {text} should be list of string.")
        text = [text]

    elif is_list_of_string(text):
        if is_split_into_words:
            text = [text]

    elif is_nested_list_of_string(text):
        if not is_split_into_words:
            raise ValueError("Type of the input {text} should be list of string.")

    else:
        raise ValueError("What the fuck are you typing as input ??!!")

    return text