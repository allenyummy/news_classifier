# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Test function of _check_input_type_and_transform

import logging
import pytest
from src.utils.check_input_type_and_transform import (
    is_string,
    is_list_of_string,
    is_nested_list_of_string,
    check_input_type_and_transform,
)

logger = logging.getLogger(__name__)


##################################################################
##### is_string, is_list_of_string, is_nested_list_of_string #####
##################################################################

test_data = [
    (
        "TEST-0",
        "我是字串。",
        {
            "is_string": True,
            "is_list_of_string": False,
            "is_nested_list_of_string": False,
        },
    ),
    (
        "TEST-1",
        123,
        {
            "is_string": False,
            "is_list_of_string": False,
            "is_nested_list_of_string": False,
        },
    ),
    (
        "TEST-2",
        ["我是字串"],
        {
            "is_string": False,
            "is_list_of_string": True,
            "is_nested_list_of_string": False,
        },
    ),
    (
        "TEST-3",
        [123, "我是字串"],
        {
            "is_string": False,
            "is_list_of_string": False,
            "is_nested_list_of_string": False,
        },
    ),
    (
        "TEST-4",
        [["123"], ["我是字串"]],
        {
            "is_string": False,
            "is_list_of_string": False,
            "is_nested_list_of_string": True,
        },
    ),
    (
        "TEST-5",
        ["123", ["我是字串"]],
        {
            "is_string": False,
            "is_list_of_string": False,
            "is_nested_list_of_string": False,
        },
    ),
    (
        "TEST-6",
        [[123], ["我是字串"]],
        {
            "is_string": False,
            "is_list_of_string": False,
            "is_nested_list_of_string": False,
        },
    ),
]


@pytest.mark.parametrize(
    argnames=("name, text, expected_ans"),
    argvalues=test_data,
    ids=[f"{i[0]}" for i in test_data],
)
def test_is_string(name, text, expected_ans):
    assert is_string(text) == expected_ans["is_string"]


@pytest.mark.parametrize(
    argnames=("name, text, expected_ans"),
    argvalues=test_data,
    ids=[f"{i[0]}" for i in test_data],
)
def test_is_list_of_string(name, text, expected_ans):
    assert is_list_of_string(text) == expected_ans["is_list_of_string"]


@pytest.mark.parametrize(
    argnames=("name, text, expected_ans"),
    argvalues=test_data,
    ids=[f"{i[0]}" for i in test_data],
)
def test_is_nested_list_of_string(name, text, expected_ans):
    assert is_nested_list_of_string(text) == expected_ans["is_nested_list_of_string"]


##################################################################
#####          Test check_input_type_and_transform           #####
##################################################################

test_data = [
    ("TEST-0", ("我是字串", False), ["我是字串"]),
    ("TEST-1", (["我是字串"], False), ["我是字串"]),
    ("TEST-2", (["我是", "字串"], False), ["我是", "字串"]),
    ("TEST-3", (["我是", "字串"], True), [["我是", "字串"]]),
    ("TEST-4", ([["我是字串"]], True), [["我是字串"]]),
    ("TEST-5", ([["我是", "字串"]], True), [["我是", "字串"]]),
]


@pytest.mark.parametrize(
    argnames=("name, input, expected_ans"),
    argvalues=test_data,
    ids=[f"{i[0]}" for i in test_data],
)
def test_check_input_type_and_transform(name, input, expected_ans):
    assert check_input_type_and_transform(input[0], input[1]) == expected_ans
