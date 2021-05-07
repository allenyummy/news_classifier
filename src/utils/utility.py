# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from typing import List, Dict, Union, Optional
import torch
from flair.data import Sentence
from src.utils import struct as st


logger = logging.getLogger(__name__)


def is_string(input):
    if isinstance(input, str):
        return True
    return False


def is_list_of_string(input):
    if isinstance(input, list) and all(isinstance(i, str) for i in input):
        return True
    return False


def is_nested_list_of_string(input):
    if isinstance(input, list):
        for i in input:
            if not isinstance(i, list):
                return False
            for j in i:
                if not isinstance(j, str):
                    return False
        return True
    return False


def transform_text(
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


def load(input: Union[str, List[str]]) -> List[str]:

    ret = list()
    if not input:
        return ret

    if not is_string(input) and not is_list_of_string(input):
        raise ValueError(f"Expected string or list of string, but got {type(input)}")

    def load_file(file_path: str):
        with open(file_path, "r", encoding="utf-8-sig") as f:
            ret = [w.rstrip() for w in f.readlines()]
            f.close()
        return ret

    if is_string(input):
        if input.endswith(".txt"):
            ret.extend(load_file(input))
        else:
            ret.append(input)

    elif is_list_of_string(input):
        for ipt in input:
            if ipt.endswith(".txt"):
                ret.extend(load_file(ipt))
            else:
                ret.append(ipt)

    return list(set(ret))


def load_stopwords(
    stopwords: Optional[Union[str, List[str]]] = None,
    load_default_stopwords: Optional[bool] = True,
) -> List[str]:

    ret = list()
    if not stopwords and not load_default_stopwords:
        return ret

    if stopwords:
        ret.extend(load(stopwords))

    if load_default_stopwords:

        """ Spacy stopwords """
        # /opt/anaconda3/envs/news_classifier/lib/python3.8/site-packages/spacy/lang/zh/stop_words.py
        from spacy.lang.zh.stop_words import STOP_WORDS as spacy_stopwords

        ret.extend(list(spacy_stopwords))  ## type(spacy_stopwords) is set.

        """ Default stopwords file path"""
        file_abs_dirname = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "stopwords"
        )
        file_path_list = [
            os.path.join(file_abs_dirname, file)
            for file in os.listdir(file_abs_dirname)
            if file.endswith(".txt")
        ]
        ret.extend(load(file_path_list))

    return list(set(ret))


def format(input: List[st.RetStruct]) -> dict:

    return {
        "NN": True if input[0].news_category == st.NewsCategory.NN else False,
        "NN_SCORE": input[0].score,
        "NN_KEYWORDS": input[0].keywords,
        "ESG": True if input[1].news_category == st.NewsCategory.NN else False,
        "ESG_SCORE": input[1].score,
        "ESG_KEYWORDS": input[1].keywords,
    }


def reshape_embedding(embedding: torch.tensor) -> torch.tensor:
    return embedding.view(1, -1)


def get_word_embedding(word_embedding_model, word: str) -> torch.tensor:
    word = Sentence(word)
    word_embedding_model.embed(word)
    word_embedding = word[0].embedding
    return word_embedding.view(1, -1)


def save_embedding(embedding: Dict[str, torch.tensor], outpath: str):
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for word, embedding in embedding.items():
        outfilepath = os.path.join(outpath, f"{word}.pt")
        torch.save(embedding, outfilepath)