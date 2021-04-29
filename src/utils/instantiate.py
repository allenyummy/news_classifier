# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Instantiate tokenizer

import logging
from src.utils import tokenization as tk

logger = logging.getLogger(__name__)


TOKENIZER_MODEL_MAP = {
    "ckiptagger": "model/ckiptagger/",
    "ckip-transformers-albert-tiny": "ckiplab/albert-tiny-chinese-ws",
    "ckip-transformers-albert-base": "ckiplab/albert-base-chinese-ws",
    "ckip-transformers-bert-base": "ckiplab/bert-base-chinese-ws",
    "bert-tokenizer": "hfl/chinese-bert-wwm",
    "spacy-zh_core_web_sm_3.0.0": "model/spacy/zh_core_web_sm-3.0.0/zh_core_web_sm/zh_core_web_sm-3.0.0/",
    "spacy-zh_core_web_md_3.0.0": "model/spacy/zh_core_web_md-3.0.0/zh_core_web_md/zh_core_web_md-3.0.0",
    "spacy-zh_core_web_lg_3.0.0": "model/spacy/zh_core_web_lg-3.0.0/zh_core_web_lg/zh_core_web_lg-3.0.0",
    "spacy-zh_core_web_trf_3.0.0": "model/spacy/zh_core_web_trf-3.0.0/zh_core_web_trf/zh_core_web_trf-3.0.0",
    "jieba": None,
    "monpa": None,
    "nltk": None,
}


def instantiate_tokenizer(tokenization_method_or_model: str):
    if tokenization_method_or_model not in TOKENIZER_MODEL_MAP:
        raise ValueError("What the fuck of the tokenization_method_or_model ?")

    model_path = TOKENIZER_MODEL_MAP[tokenization_method_or_model]

    if tokenization_method_or_model == "ckiptagger":
        tokenizer = tk.Ckip_Tagger_Tokenizer(model_path)

    elif tokenization_method_or_model == "ckip-transformers-albert-tiny":
        tokenizer = tk.Ckip_Transformers_Tokenizer(level=1)

    elif tokenization_method_or_model == "ckip-transformers-albert-base":
        tokenizer = tk.Ckip_Transformers_Tokenizer(level=2)

    elif tokenization_method_or_model == "ckip-transformers-bert-base":
        tokenizer = tk.Ckip_Transformers_Tokenizer(level=3)

    elif tokenization_method_or_model == "spacy-zh_core_web_sm_3.0.0":
        tokenizer = tk.Spacy_Chinese_Tokenizer(model_path)

    elif tokenization_method_or_model == "spacy-zh_core_web_md_3.0.0":
        tokenizer = tk.Spacy_Chinese_Tokenizer(model_path)

    elif tokenization_method_or_model == "spacy-zh_core_web_lg_3.0.0":
        tokenizer = tk.Spacy_Chinese_Tokenizer(model_path)

    elif tokenization_method_or_model == "spacy-zh_core_web_trf_3.0.0":
        tokenizer = tk.Spacy_Chinese_Tokenizer(model_path)

    elif tokenization_method_or_model == "jieba":
        tokenizer = tk.Jieba_Tokenizer()

    elif tokenization_method_or_model == "monpa":
        tokenizer = tk.Monpa_Tokenizer()

    elif tokenization_method_or_model == "bert-tokenizer":
        tokenizer = tk.Bert_Tokenizer(model_path)

    return tokenizer