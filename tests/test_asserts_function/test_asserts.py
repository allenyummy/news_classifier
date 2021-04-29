# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Test for asserts function

import logging
import pytest
import tests.asserts as ass

logger = logging.getLogger(__name__)

test_data_list_of_list_of_string = [
    ("TEST-1", [["我", "是", "江侑倫", "。"]], True),
    ("TEST-2", ["空白", " ", "也", "是", "可以", "的", "~"], False),
    ("TEST-3", [["英文", "名稱", 1, "Allen"]], False),
    ("TEST-4", "英文", False),
]

test_data_exact_same_lists = [
    ("TEST-1", ([["我", "是", "江侑倫", "。"]], [["我", "是", "江侑倫", "。"]]), True),
    ("TEST-2", ([["我", "是", "江侑倫", "。"]], [["我", "江侑倫", "。"]]), False),
    ("TEST-3", ([["我", "是", "江侑倫", "。"]], [["我", "是江" "侑倫", "。"]]), False),
    ("TEST-4", ([["我", "是", "江侑倫", "。"]], []), False),
]


@pytest.mark.parametrize(
    argnames=("name, input, expected_ans"),
    argvalues=test_data_list_of_list_of_string,
    ids=[f"{i[0]}" for i in test_data_list_of_list_of_string],
)
def test_assert_ListOfListOfString(name, input, expected_ans):
    assert ass.assert_ListOfListOfString(input) == expected_ans


@pytest.mark.parametrize(
    argnames=("name, input, expected_ans"),
    argvalues=test_data_exact_same_lists,
    ids=[f"{i[0]}" for i in test_data_exact_same_lists],
)
def test_assert_ExactSameLists(name, input, expected_ans):
    assert ass.assert_ExactSameLists(input[0], input[1]) == expected_ans
