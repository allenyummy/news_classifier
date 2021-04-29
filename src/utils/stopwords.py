# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Read All Stop Words

import logging
import os
from typing import Union, List, Optional
from spacy.lang.zh.stop_words import STOP_WORDS as spacy_stopwords
from src.utils.check_input_type_and_transform import is_string, is_list_of_string

logger = logging.getLogger(__name__)


def get_stopwords(
    stopwords: Optional[Union[str, List[str]]] = None,
    add_spacy_stopwords: Optional[bool] = True,
) -> List[str]:

    if stopwords and not is_string(stopwords) and not is_list_of_string(stopwords):
        raise ValueError(
            f"Expected string or list of string, but got {type(stopwords)}"
        )

    stopwords_set = set()
    if not stopwords or stopwords.endswith(".txt"):
        stopwords_set = get_stopwords_from_file(stopwords)
    else:
        stopwords_set = get_stopwords_from_string_or_list(stopwords)

    if add_spacy_stopwords:
        stopwords_set.update(spacy_stopwords)

    return list(stopwords_set)


def get_stopwords_from_string_or_list(stopwords: Union[str, List[str]]) -> set:

    if is_string(stopwords):
        stopwords = [stopwords]

    return set(stopwords)


def get_stopwords_from_file(
    filename_or_filelist: Optional[Union[str, List[str]]]
) -> set:

    if is_string(filename_or_filelist):
        filename_or_filelist = [filename_or_filelist]

    file_abs_dirname = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "stopwords_file"
    )
    file_end = r".txt"

    candidate_file = list()
    for file in os.listdir(file_abs_dirname):
        if file.endswith(file_end):
            if not filename_or_filelist:
                candidate_file.append(file)
            elif filename_or_filelist and file in filename_or_filelist:
                candidate_file.append(file)

    stopwords_set = set()
    for file in candidate_file:
        file_path = os.path.join(file_abs_dirname, file)
        with open(file_path, "r", encoding="utf-8") as f:
            stopwords_list = [w.rstrip() for w in f.readlines()]
            f.close()
        stopwords_set.update(stopwords_list)

    return stopwords_set
