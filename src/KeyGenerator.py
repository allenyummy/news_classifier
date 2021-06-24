# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: KeyGenerator aims to generate words that are related to a given word.

import json
import logging
import os
from datetime import datetime
from typing import Dict, Optional

from gensim.models import KeyedVectors, word2vec
from tqdm import tqdm

from src.base import BaseGenerator
from src.utils import struct as st

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


MODEL_PATH = {
    "20210603040434": {
        "normal": "model/word2vec/word2vec_20210603040434_v250_c5_e5_s1.model",
        "fast": "model/word2vec/word2vec_20210603040434_v250_c5_e5_s1.wordvectors",
    }
}


class Word2VecKeyGenerator(BaseGenerator):
    """A Word2Vec-based KeyGenerator"""

    def __init__(
        self,
        modelkey: str,
        use_fast: Optional[bool] = True,
    ):
        """
        Init Word2VecKeyGenerator.
        It can generate words that are related to a given words by using a Word2Vec trained model.

        Args:
            `modelkey`: A key to choose a specific Word2Vec model.
            `use_fast`: Whether to use fast mode. It's a special function in the gensim library.
        Type:
            `modelkey`: string
            `use_fast`: bool (default = True)
        Return:
            None
        """

        logger.debug(f"Init model (use_fast: {use_fast}) & results.")
        self.modelkey = modelkey
        self.use_fast = use_fast

        if use_fast:
            wv = KeyedVectors.load(MODEL_PATH[modelkey]["fast"], mmap="r")
        else:
            model = word2vec.Word2Vec.load(MODEL_PATH[modelkey]["normal"])
            wv = model.wv
        self.wv = wv
        self.init_results()

    def infer(
        self,
        input: str,
        topn: Optional[int] = 10,
        threshold: Optional[float] = 0.70,
        force_info: Optional[Dict[str, Dict[str, float]]] = None,
        init_results: Optional[bool] = True,
    ) -> st.KeyGeneratorStruct:
        """
        Infer for a txt file or a single word.

        Args:
            `input`       : A txt file or a single word.
            `topn`        : Top n words that are related to a given word.
                            It's a global variable for all words if input is a txt file.
            `threshold`   : Threshold of cosine similarity (cs) score.
                            It's also a global variable for all words if input is a txt file.
                            If a cs score of candidate word is smaller than a given threshold,
                            it would not be an answer we want, even if it's one of top n words.
            `force_info`  : A force information sets custom topn and threshold for a specific word.
                            If input is a txt file (contains lots of words)
                            and you want to set a specific topn and threshold for a specific word,
                            it could be set in the force_info.
                            e.g.
                            force_info = {
                                "暴力": {
                                    "topn": 7,
                                    "threshold": 0.58,
                                }
                                "大跌": {
                                    "topn": 14,
                                    "threshold: 0.77,
                                }
                            }
            `init_results`: Whether to init results obtained in previous `infer` call.
        Type:
            `input`       : string
            `topn`        : integer
            `threshold`   : float
            `force_info`  : dict
            `init_results`: bool
        Return:
            Inference results.
            rtype: st.KeyGeneratorStruct
        """

        if init_results:
            self.init_results()

        self.results.default_info = {"topn": topn, "threshold": threshold}
        self.results.base.append(input)
        self.results.force_info = force_info

        if input.endswith(".txt"):
            logger.debug(f"Processing {input} as A TXT FILE.")
            self.results.results.update(
                self.infer_a_file(input, topn, threshold, force_info)
            )
        else:
            logger.debug(f"Processing {input} as A SINGLE WORD.")
            self.results.results.update(self.infer_a_word(input, topn, threshold))

        return self.results

    def infer_a_file(
        self,
        file: str,
        topn: Optional[int] = 10,
        threshold: Optional[float] = 0.70,
        force_info: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> Dict[str, st.KeyGenerator_WordStruct]:
        """
        Infer a txt file that contains lots of words.
        The format of a txt file is one word per line:
            人口販賣
            入獄
            上訴
            下市
            大跌
            不肖
            ...

        Args: Please Check in the `infer` function.
        Type: Please Check in the `infer` function.
        Return:
            Inference results of all words in a given txt file.
            rtype: dict [string, st.KeyGenerator_WordStruct]
        """

        ret = dict()
        lines = open(file, "r", encoding="utf-8-sig").readlines()
        for word in tqdm(lines, total=(len(lines)), desc="Inference"):
            word = word.strip()

            ## If word exists in ret dict, it means that the input file contains duplicate words.
            ## Just skip it.
            if word in ret:
                pass

            ## If word exists in force_info dict,
            ## it means we need to use custom topn and threshold for this word.
            if force_info and word in force_info:
                word_ret = self.infer_a_word(
                    word,
                    force_info[word]["topn"],  # custom topn for this word
                    force_info[word]["threshold"],  # custom threshold for this word
                )
            else:
                word_ret = self.infer_a_word(word, topn, threshold)
            ret.update(word_ret)
        return ret

    def infer_a_word(
        self,
        word: str,
        topn: Optional[int] = 10,
        threshold: Optional[float] = 0.70,
    ) -> Dict[str, st.KeyGenerator_WordStruct]:
        """
        Infer a single word.

        Args: Please Check in the `infer` function.
        Type: Please Check in the `infer` function.
        Return:
            Inference results of a given words.
            rtype: dict [string, st.KeyGenerator_WordStruct]
        """

        ret = {word: st.KeyGenerator_WordStruct(topn=topn, threshold=threshold)}

        ## Protection mode
        ## Another api: site-packages/gensim/models/keyedvectors.py, line 396, in get_index
        if word not in self.wv:
            ret[word].debug = f"{word} never appeared before."
            return ret

        ## Be careful for list (call for value/reference).
        [
            ret[word].related.append((relatedword, round(cs_score, 2)))
            for (relatedword, cs_score) in self.wv.most_similar(
                positive=[word], negative=None, topn=topn
            )
            if cs_score >= threshold
        ]

        related_word_cnt = len(ret[word].related)
        if related_word_cnt == 0:
            ret[word].debug = "Not found."
        elif related_word_cnt < topn:
            ret[word].debug = f"related_word_cnt: {related_word_cnt} < topn: {topn}"
        return ret

    def save(self, outfile: str):
        """
        Save inference results into outfile. Support extension of .txt and .json.

        Args:
            `outfile`: A output file to store inference results.
        Type:
            `outfile`: string
        Return:
            None
        """

        dirname = os.path.dirname(os.path.abspath(outfile))
        filename = os.path.basename(outfile)

        if not os.path.exists(dirname):
            logger.debug(f"Create directory: {dirname}")
            os.makedirs(dirname)

        if filename.endswith(".txt"):
            logger.debug(f"Save2TXT: {outfile}")
            self.save2txt(outfile)

        elif filename.endswith(".json"):
            logger.debug(f"Save2Json: {outfile}")
            self.save2json(outfile)

        else:
            raise ValueError(
                f"{filename} is NOT supported. Only support either .txt or .json."
            )

    def save2txt(self, outfile: str):
        """
        Save inference results into outfile whose extension is .txt.

        Args:
            `outfile`: A output file to store inference results.
        Type:
            `outfile`: string
        Return:
            None
        """

        res_set = set()
        for _, wordstruct in self.results.results.items():
            for related in wordstruct.related:
                relatedword = related[0]
                res_set.add(relatedword)

        with open(outfile, "w", encoding="utf-8") as fo:
            for relatedword in tqdm(res_set, total=len(res_set), desc="Write2TXT"):
                fo.write(relatedword + "\n")
            fo.close()

    def save2json(self, outfile: str):
        """
        Save inference results into outfile whose extension is .json.

        Args:
            `outfile`: A output file to store inference results.
        Type:
            `outfile`: string
        Return:
            None
        """

        with open(outfile, "w", encoding="utf-8") as fo:
            json.dump(self.results.__2dict__(), fo, ensure_ascii=False, indent=4)
            fo.close()

    def save2graph(self):
        pass

    def relatedwords(self, word) -> st.KeyGenerator_WordStruct:
        """
        Related words for a given word. It should be used after calling `infer` function.

        Args:
            `word`: a input word.
        Type:
            `word`: string
        Return:
            Inference results for a given word.
            rtype: st.KeyGenerator_WordStruct
        """

        return self.results.results[word]

    def init_results(self):
        """
        Init results.
        """

        self.results = st.KeyGeneratorStruct(
            createtime=datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            modelkey=self.modelkey,
            use_fast=self.use_fast,
        )


if __name__ == "__main__":

    w2v = Word2VecKeyGenerator(modelkey="20210603040434")
    topn = 10
    threshold = 0.60
    # force_info = {
    #     "暴力": {
    #         "topn": 10,
    #         "threshold": 0.44,
    #     }
    # }

    """ NN """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    nn_file = "src/utils/keywords/negative_news/NN_keywords.txt"
    nn_outfile_json = f"src/utils/keywords/negative_news/NN_keywords_{now}.json"
    nn_outfile_txt = f"src/utils/keywords/negative_news/NN_keywords_{now}.json"
    w2v.infer(nn_file, topn, threshold, force_info=None, init_results=True)
    # w2v.save2json(outfile=nn_outfile_json)
    # w2v.save2txt(outfile=nn_outfile_txt)

    """ ESG """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    esg_file = "src/utils/keywords/esg_news/ESG_keywords.txt"
    esg_outfile_json = f"src/utils/keywords/esg_news/ESG_keywords_{now}.json"
    esg_outfile_txt = f"src/utils/keywords/esg_news/ESG_keywords_{now}.txt"
    w2v.infer(esg_file, topn, threshold, force_info=None, init_results=True)
    # w2v.save2json(outfile=esg_outfile_json)
    # w2v.save2txt(outfile=esg_outfile_txt)
