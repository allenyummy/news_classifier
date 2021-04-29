# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: compare NN keywords and keywords extracted by keyExtractor

import logging
import os
from typing import List, Union, Optional, Dict
import torch
from flair.data import Sentence
from flair.embeddings import TransformerWordEmbeddings
from src.utils import (
    struct as st,
    evaluation as ev,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class keyComparator:
    def __init__(
        self,
        embedding_method_or_model: str,
        ground_file_path: str,
        save_ground_embeddings: Optional[bool] = True,
        use_cache_ground_embeddings: Optional[bool] = False,
        cache_ground_path: Optional[str] = "model/keywords",
    ):
        """ Init TransformerWordEmbeddings model """
        self.word_embedding_model = TransformerWordEmbeddings(embedding_method_or_model)

        """ Get ground keywrods """
        with open(ground_file_path, "r", encoding="utf-8-sig") as f:
            self.ground_keywords = [keyword.strip() for keyword in f]

        """ Get ground embeddings """
        self.ground = dict()
        if use_cache_ground_embeddings:

            if not os.path.exists(cache_ground_path):
                raise ValueError(f"{cache_ground_path} does not exist...")

            for file in os.listdir(cache_ground_path):
                keyword = file.split(".")[0]
                filepath = os.path.join(cache_ground_path, file)
                word_embedding = torch.load(filepath)
                self.ground[keyword] = word_embedding

            for keyword in self.ground_keywords:
                if keyword not in self.ground:
                    word_embedding = self._get_word_embedding(keyword)
                    self.ground[keyword] = word_embedding

        else:

            for keyword in self.ground_keywords:
                word_embedding = self._get_word_embedding(keyword)
                self.ground[keyword] = word_embedding

            if not save_ground_embeddings:
                logger.warning("Why not saving word embedding ?????")

            else:
                self._save_embedding(cache_ground_path)
                logger.info(f"Save embedding into {cache_ground_path}.")

    def evaluate(
        self,
        keyword_lists: List[List[st.KeyStruct]],
        threshold: Optional[float] = 0.6,  # cosine 45~60 degree
        top_n_ground: Optional[int] = 5,
    ) -> List[List[float]]:

        result_lists = list()
        for keyword_list in keyword_lists:
            result_list = list()
            for keystruct in keyword_list:
                result = {
                    "id": keystruct.id,
                    "keyword": keystruct.keyword,
                    "score": keystruct.score,
                    "ground_keywords": list(),
                }
                record = list()
                for ground_keyword, ground_keyword_embedding in self.ground.items():
                    score = ev.cosineSimilarity(
                        keystruct.embedding, ground_keyword_embedding
                    )
                    if score >= threshold:
                        record.append((ground_keyword, score))
                record = sorted(record, key=lambda k: k[1], reverse=True)
                record = record[: min(top_n_ground, len(record))]
                for r in record:
                    result["ground_keywords"].append(
                        {
                            "keyword": r[0],
                            "score": r[1],
                        }
                    )
                result_list.append(result)
            result_lists.append(result_list)
        return result_lists

    def _get_word_embedding(
        self,
        word: str,
    ) -> torch.tensor:
        word = Sentence(word)
        self.word_embedding_model.embed(word)
        word_embedding = word[0].embedding
        word_embedding = self._reshape_embedding(word_embedding)
        return word_embedding

    def _reshape_embedding(self, embedding: torch.tensor) -> torch.tensor:
        return embedding.view(1, -1)  ## [1, 768]

    def _save_embedding(self, outpath: str):
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        for word, embedding in self.ground.items():
            outfilepath = os.path.join(outpath, f"{word}.pt")
            torch.save(embedding, outfilepath)


if __name__ == "__main__":

    co = keyComparator(
        embedding_method_or_model="ckiplab/bert-base-chinese",
        ground_file_path="docs/NN_keywords.txt",
        use_cache_ground_embeddings=True,
        cache_ground_path="model/keywords",
    )

    from src.keyExtractor import keyExtractor

    ke = keyExtractor(
        tokenization_method_or_model="ckiptagger",
        embedding_method_or_model="ckiplab/bert-base-chinese",
    )
    text = "詐欺犯吳朱傳甫獲釋又和同夥林志成假冒檢警人員，向新營市黃姓婦人詐財一百八十萬元，事後黃婦驚覺上當報警處理，匯寄的帳戶被列警示帳戶，凍結資金往返；四日兩嫌再冒名要黃婦領五十萬現金交付，被埋伏的警員當場揪住。"
    text = "報導指出，這起詐騙事件行騙對象主要是馬來西亞華人，嫌犯於2011年7月至9月間撥打6857通馬來西亞電話，詐騙金額人民幣3615.7萬元。"
    text = "晶圓代工龍頭台積電日前核准資本預算28.87億美元，將在中國南京廠擴建28奈米成熟製程產能，卻引起中國通信業分析師項立剛強烈反對，\
            指此舉將打擊中國晶片產業。中國國台辦發言人馬曉光今日表示，相信中國是法治國家，會依法辦事，依法依規來處理。項立剛日前發表「強烈呼籲制止台積電南京廠擴產」一文，\
            稱台積電正在推行高端晶片控制、低端晶片傾銷壓制的策略，呼籲中國官方進行研究、審查，保護中國晶片製造企業，防止台積電的市場壟斷行為。\
            今日在國台辦例行記者會上，有媒體提問，台積電日前宣佈要在南京擴產28奈米全球製程產能帶，中芯國際日前也曾宣佈要在深圳合作擴產28奈米晶片製程，\
            中國有專家表示，台積電擴產或對中芯國際產生排擠競爭效應，還有學者呼籲中國應禁止台積電這個方案，請問對此有何評論？馬曉光則回應，「相信我們是法治國家，會依法辦事，依法依規來處理」。\
            他強調，關於台資台企來中國投資，有完備的法律、法規和管理機制，對於具體個案，有關部門會科學評估，依法依規處理。"
    text = "墾丁悠活麗緻渡假村的三至六區以集合住宅名義興建，目前仍屬停業狀態，僅一、二區共161間房正常營業。屏東縣政府觀光傳播處指出，業者正在辦理使用執照變更成為旅館用途，日前已經通過環評，但仍待墾丁國家公園管理處核准開發許可，最終還需回到縣府申請旅館登記證，屆時才能恢復營業。"
    text = "悠活渡假公司前董事長曾忠信涉及掏空公司資產、詐領資策會補助款及故買盜伐林木等3案件，不法獲益上億元，台南地檢署歷經1年多的偵查，29日將曾忠信等6人依違反證交法、詐欺、背信罪及故買贓物等罪起訴，並請法官從重量刑。"
    keyword_lists = ke.extract_keywords(text, n_gram=2, top_n=10)

    result_lists = co.evaluate(keyword_lists)
    for result_list in result_lists:
        for result in result_list:
            print(result)
            print()
