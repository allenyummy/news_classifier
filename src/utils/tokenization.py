# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Tokenizaton

import logging
from abc import ABC, abstractmethod
from typing import List, Union
from ckip_transformers.nlp import CkipWordSegmenter
from ckiptagger import data_utils, construct_dictionary, WS
from transformers import AutoTokenizer
import spacy
import jieba
import monpa

logger = logging.getLogger(__name__)


class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:
        raise NotImplementedError


class Ckip_Transformers_Tokenizer(Tokenizer):

    MODEL_NAME_ON_HUGGINGFACE_MODEL_HUB = {
        1: "ckiplab/albert-tiny-chinese-ws",
        2: "ckiplab/albert-base-chinese-ws",
        3: "ckiplab/bert-base-chinese-ws",
    }

    def __init__(self, level: int = 1, device: int = -1):
        if level not in self.MODEL_NAME_ON_HUGGINGFACE_MODEL_HUB.keys():
            raise ValueError(
                f"Expect {self.MODEL_NAME_ON_HUGGINGFACE_MODEL_HUB.keys()} but got {level}."
            )
        self.ws_model = CkipWordSegmenter(level=level, device=device)

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:

        if isinstance(text, str):
            text = [text]
        elif isinstance(text, list):
            pass
        else:
            raise ValueError(
                f"Expect text type (str or List[str]) but got {type(text)}"
            )
        tokenized_text = self.ws_model(text)
        return tokenized_text


class Ckip_Tagger_Tokenizer(Tokenizer):
    def __init__(self, model_path: str):
        self.ws_model = WS(model_path)

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:

        if isinstance(text, str):
            text = [text]
        elif isinstance(text, list):
            pass
        else:
            raise ValueError(
                f"Expect text type (str or List[str]) but got {type(text)}"
            )
        tokenized_text = self.ws_model(text)
        return tokenized_text


class Bert_Tokenizer(Tokenizer):
    def __init__(self, model_path: str):
        self.ws_model = AutoTokenizer.from_pretrained(model_path, use_fast=True)

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:
        if isinstance(text, str):
            tokenized_text = [self.ws_model(text)]

        elif isinstance(text, list):
            tokenized_text = list()
            for doc_text in text:
                doc = [self.ws_model.tokenize(doc_text)]
                tokenized_text.append(doc)
        else:
            raise ValueError(
                f"Expect text type (str or List[str]) but got {type(text)}"
            )
        return tokenized_text


class Spacy_Chinese_Tokenizer(Tokenizer):
    def __init__(self, model_path: str):
        self.ws_model = spacy.load(model_path)

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:

        if isinstance(text, str):
            doc = self.ws_model(text)
            tokenized_text = [[token.text for token in doc]]

        elif isinstance(text, list):
            tokenized_text = list()
            for doc_text in text:
                doc = self.ws_model(doc_text)
                res = [token.text for token in doc]
                tokenized_text.append(res)
        else:
            raise ValueError(
                f"Expect text type (str or List[str]) but got {type(text)}"
            )
        return tokenized_text


class Jieba_Tokenizer(Tokenizer):
    def __init__(self):
        pass

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:

        if isinstance(text, str):
            doc = jieba.cut(text)
            tokenized_text = [[token for token in doc]]

        elif isinstance(text, list):
            tokenized_text = list()
            for doc_text in text:
                doc = jieba.cut(doc_text)
                res = [token for token in doc]
                tokenized_text.append(res)
        else:
            raise ValueError(
                f"Expect text type (str or List[str]) but got {type(text)}"
            )
        return tokenized_text


class Monpa_Tokenizer(Tokenizer):
    def __init__(self):
        pass

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:

        if isinstance(text, str):
            doc = monpa.cut(text)
            tokenized_text = [[token for token in doc]]

        elif isinstance(text, list):
            tokenized_text = list()
            for doc_text in text:
                doc = monpa.cut(doc_text)
                res = [token for token in doc]
                tokenized_text.append(res)
        else:
            raise ValueError(
                f"Expect text type (str or List[str]) but got {type(text)}"
            )
        return tokenized_text


class NLTK_Tokenizer(Tokenizer):
    def __init__(self):
        raise NotImplementedError

    def tokenize(self, text: Union[str, List[str]]) -> List[List[str]]:
        raise NotImplementedError
