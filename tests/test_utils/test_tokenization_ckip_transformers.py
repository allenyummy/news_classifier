# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Test for tokenization

import logging
import pytest
import tests.asserts as ass
from src.utils.tokenization import Ckip_Transformers_Tokenizer

logger = logging.getLogger(__name__)

################################################################################################
##### Test Tokenization of Ckip Transformers (albert_tiny, albert_base, bert_base_chinese) #####
################################################################################################

test_data = [
    ("TEST-全中文", "我是江侑倫。", [["我", "是", "江侑倫", "。"]]),
    ("TEST-空白相間", "空白 也是可以的~", [["空白", " ", "也", "是", "可以", "的", "~"]]),
    ("TEST-中英夾雜", "英文名稱是Allen", [["英文", "名稱", "是", "Allen"]]),
    (
        "TEST-多文本",
        ["我是江侑倫。", "英文名稱是Allen"],
        [["我", "是", "江侑倫", "。"], ["英文", "名稱", "是", "Allen"]],
    ),
]


@pytest.fixture(scope="function")
def ckip_ws_model_albert_tiny():
    model = Ckip_Transformers_Tokenizer(
        ckip_model_name="ckiplab/albert-tiny-chinese-ws"
    )
    return model


@pytest.fixture(scope="function")
def ckip_ws_model_albert_base():
    model = Ckip_Transformers_Tokenizer(
        ckip_model_name="ckiplab/albert-base-chinese-ws"
    )
    return model


@pytest.fixture(scope="function")
def ckip_ws_model_bert_base():
    model = Ckip_Transformers_Tokenizer(ckip_model_name="ckiplab/bert-base-chinese-ws")
    return model


@pytest.mark.parametrize(
    argnames=("name, text, expected_tokenized_text"),
    argvalues=test_data,
    ids=[f"CKIP_ALBERT_TINY, {i[0]}" for i in test_data],
)
def test_ckip_ws_model_albert_tiny_tokenizer(
    ckip_ws_model_albert_tiny, name, text, expected_tokenized_text
):
    tokenized_text = ckip_ws_model_albert_tiny.tokenize(text)
    assert ass.assert_ListOfListOfString(tokenized_text)
    assert ass.assert_ExactSameLists(tokenized_text, expected_tokenized_text)


@pytest.mark.parametrize(
    argnames=("name, text, expected_tokenized_text"),
    argvalues=test_data,
    ids=[f"CKIP_ALBERT_BASE, {i[0]}" for i in test_data],
)
def test_ckip_ws_model_albert_base_tokenizer(
    ckip_ws_model_albert_base, name, text, expected_tokenized_text
):
    tokenized_text = ckip_ws_model_albert_base.tokenize(text)
    assert ass.assert_ListOfListOfString(tokenized_text)
    assert ass.assert_ExactSameLists(tokenized_text, expected_tokenized_text)


@pytest.mark.parametrize(
    argnames=("name, text, expected_tokenized_text"),
    argvalues=test_data,
    ids=[f"CKIP_BERT_BASE, {i[0]}" for i in test_data],
)
def test_ckip_ws_model_bert_base_tokenizer(
    ckip_ws_model_bert_base, name, text, expected_tokenized_text
):
    tokenized_text = ckip_ws_model_bert_base.tokenize(text)
    assert ass.assert_ListOfListOfString(tokenized_text)
    assert ass.assert_ExactSameLists(tokenized_text, expected_tokenized_text)
