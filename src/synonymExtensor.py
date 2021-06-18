# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Synonyms Extensor

import logging
import os
from typing import List, Tuple, Dict, Union, Optional
from collections import defaultdict
import torch
from flair.data import Sentence
from flair.embeddings import TransformerWordEmbeddings
from src.utils import tokenization as tk, utility as ut, struct as st, evaluation as ev
from src.utils.keywords import keywords as ke

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class synonymExtensor:
    def __init__(
        self,
        tokenization_method_or_model: str,
        embedding_method_or_model: str,
        category: str,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
        load_cache: Optional[bool] = True,
        save_cache: Optional[bool] = False,
        cache_dir: Optional[str] = "model/keywords/",
    ):

        """ Init """
        self.tokenizer = tk.TokenizerFactory(tokenization_method_or_model)
        self.word_embedding_model = TransformerWordEmbeddings(embedding_method_or_model)

        """ Load Keywords of category """
        self.category = category
        self._keywords = ke.KeywordsFactory(
            name=category, keywords=keywords, load_default=load_default
        ).keywords
        self._keywords = list(self._keywords)

        """ Get/Load/Save Keywords Embeddings """
        cache_dir = os.path.join(cache_dir, self.category.lower())
        self._keywords_embeddings = self._load_embeddings(load_cache, cache_dir)
        if save_cache:
            ut.save_embedding(self._keywords_embeddings, cache_dir)

    def extract(
        self,
        text: Union[str, List[str], List[List[str]]],
        is_split_into_words: Optional[bool] = False,
        stopwords: Optional[Union[str, List[str]]] = None,
        load_default_stopwords: Optional[bool] = True,
        keyword: Optional[str] = None,
        threshold: Optional[float] = 0.78,
        top_n: Optional[int] = 5,
    ) -> List[List[st.KeyStruct]]:

        """ Preprocess """
        tokenized_docs, content_docs = self._preprocess(
            text, is_split_into_words, stopwords, load_default_stopwords
        )

        """ Get embeddings and calculate score """
        logger.debug("===== GET EMBEDDINGS & CALCULATE SCORE =====")
        ret_list = list()
        for tokenized_doc, content_doc in zip(tokenized_docs, content_docs):
            ret = defaultdict(list)
            doc = Sentence(tokenized_doc)
            self.word_embedding_model.embed(doc)

            if keyword:
                keyword_embedding = self.keyword_embedding(keyword)
                for (idx, token) in content_doc:
                    token_embedding = doc[idx].embedding
                    cs_score = ev.cosineSimilarity(keyword_embedding, token_embedding)
                    if cs_score >= threshold:
                        ret[keyword].append(
                            st.KeyStruct(idx, token, cs_score, token_embedding)
                        )
                        logger.debug(f"{keyword} -> {token} {cs_score}")

            else:
                for keyword, keyword_embedding in self._keywords_embeddings.items():
                    for (idx, token) in content_doc:
                        token_embedding = doc[idx].embedding
                        cs_score = ev.cosineSimilarity(
                            keyword_embedding, token_embedding
                        )
                        if cs_score >= threshold:
                            ret[keyword].append(
                                st.KeyStruct(idx, token, cs_score, token_embedding)
                            )
                            logger.debug(f"{keyword} -> {token} {cs_score}")

            ret_list.append(ret)

        return ret_list

    @property
    def keywords(self) -> Tuple[str]:
        return tuple(self._keywords)

    def keyword_embedding(self, keyword: str):
        ## Be careful to use it. Don't assign value to it.
        ## It only support as a look-up table.
        try:
            return self._keywords_embeddings[keyword]
        except:
            self._keyword_embedding[keyword] = ut.get_word_embedding(
                self.word_embedding_model, keyword
            )
            return self._keywords_embeddings[keyword]

    def _load_embeddings(self, load_cache, cache_dir) -> Dict[str, torch.tensor]:

        keywords_embeddings = dict()
        cache_keywords = list()

        if load_cache:
            cache_dir = os.path.join(cache_dir)
            if not os.path.exists(cache_dir):
                raise ValueError(f"{cache_dir} is not found.")
            cache_keywords = [file.split(".")[0] for file in os.listdir(cache_dir)]
            self._keywords.extend(
                [
                    cache_keyword
                    for cache_keyword in cache_keywords
                    if cache_keyword not in self._keywords
                ]
            )

        for keyword in self.keywords:
            ## IF load_cache, THEN cache_keywords is [].
            if keyword in cache_keywords:
                file = f"{keyword}.pt"
                word_embedding = torch.load(os.path.join(cache_dir, file))
            else:
                word_embedding = ut.get_word_embedding(
                    self.word_embedding_model, keyword
                )
            keywords_embeddings[keyword] = word_embedding

        return keywords_embeddings

    def _preprocess(
        self,
        text: Union[str, List[str], List[List[str]]],
        is_split_into_words: Optional[bool] = False,
        stopwords: Optional[Union[str, List[str]]] = None,
        load_default_stopwords: Optional[bool] = True,
    ) -> Union[List[List[str]], List[List[Tuple[int, str]]]]:

        """ Check and Transform """
        logger.debug("===== CHECK AND TRANSFORM =====")
        text = ut.transform_text(text, is_split_into_words)
        logger.debug(text)

        """ Tokenize documents """
        logger.debug("===== TOKENIZATION =====")
        if not is_split_into_words:
            tokenized_docs = self.tokenizer.tokenize(text)
        else:
            tokenized_docs = text
        logger.debug(tokenized_docs)

        """ Get stopwords """
        logger.debug("===== GET STOPWORDS ====")
        stopwords_list = ut.load_stopwords(
            stopwords, load_default_stopwords=load_default_stopwords
        )
        logger.debug(f"stopwords size: {len(stopwords_list)}")

        """ Get content words by removing stopwords """
        logger.debug("===== GET CONTENT WORDS BY REMOVING STOPWORDS =====")
        content_docs = list()
        for tokenized_doc in tokenized_docs:
            content_doc = list()
            for i, token in enumerate(tokenized_doc):
                if token not in stopwords_list:
                    content_doc.append((i, token))
            content_docs.append(content_doc)
        logger.debug(content_docs)

        return tokenized_docs, content_docs


if __name__ == "__main__":

    se = synonymExtensor(
        tokenization_method_or_model="ckiptagger",
        embedding_method_or_model="ckiplab/bert-base-chinese",
        category="Negative_News",
    )

    text = "詐欺犯吳朱傳甫獲釋又和同夥林志成假冒檢警人員，向新營市黃姓婦人詐財一百八十萬元，事後黃婦驚覺上當報警處理，匯寄的帳戶被列警示帳戶，凍結資金往返；四日兩嫌再冒名要黃婦領五十萬現金交付，被埋伏的警員當場揪住。"
    text = "悠活渡假公司前董事長曾忠信涉及掏空公司資產、詐領資策會補助款及故買盜伐林木等3案件，不法獲益上億元，台南地檢署歷經1年多的偵查，29日將曾忠信等6人依違反證交法、詐欺、背信罪及故買贓物等罪起訴，並請法官從重量刑。"
    # text = "法尼新創科技股份有限公司負責人田書旗、黃淑霞夫妻倆，涉嫌以投資「乙太幣拓礦礦機」、「認購飲料店、咖啡店、火鍋店及餐廳之股份」等名義，吸引民眾投資，估計違法吸金17億餘元，受害投資民眾恐多達2000人，桃園地檢署今天偵結，已依違反銀行法、非法經營期貨經理事業等罪嫌，將田書旗夫妻與員工共13人提起公訴。田書旗（40歲）、黃淑霞（42歲）從106年7月起，設計「乙太幣拓礦礦機」、「認購公司股份或特別股股份」、「認購飲料店、咖啡店、火鍋店及餐廳之股份」、「購買奇歐外匯期貨」等方案，由陳育勝等人擔任講師，四處召開說明會，以每年有18%到86%不等的高獲利，吸引民眾投資。透過說明會、網路與通訊軟體發布的訊息，田書旗夫妻倆迅速吸收許多民眾加入投資行列，檢方說，夫妻倆以「吸後金補前金」的方式，按約定將紅利撥付給投資民眾，其餘款項全挪為己用。桃園地檢署接獲檢舉後，指揮法務部調查局台北市調查處追查，偵結前已查證262位投資民眾，而他們的總投資金額已高達3億3500餘萬元，檢方說，比對扣案檔案、外部金流等資料，估計田書旗夫妻倆吸金總金額高達17億元，投資民眾被牽連受害的恐怕超過2000人，已因田書旗等人違反非銀行法「不得經營準收受存款業務達1億元以上」、「非法經營期貨經理事業」等罪嫌，將他們提起公訴。"
    # text = "墾丁悠活麗緻渡假村的三至六區以集合住宅名義興建，目前仍屬停業狀態，僅一、二區共161間房正常營業。屏東縣政府觀光傳播處指出，業者正在辦理使用執照變更成為旅館用途，日前已經通過環評，但仍待墾丁國家公園管理處核准開發許可，最終還需回到縣府申請旅館登記證，屆時才能恢復營業。"
    # text = "晶圓代工龍頭台積電日前核准資本預算28.87億美元，將在中國南京廠擴建28奈米成熟製程產能，卻引起中國通信業分析師項立剛強烈反對，\
    #         指此舉將打擊中國晶片產業。中國國台辦發言人馬曉光今日表示，相信中國是法治國家，會依法辦事，依法依規來處理。項立剛日前發表「強烈呼籲制止台積電南京廠擴產」一文，\
    #         稱台積電正在推行高端晶片控制、低端晶片傾銷壓制的策略，呼籲中國官方進行研究、審查，保護中國晶片製造企業，防止台積電的市場壟斷行為。\
    #         今日在國台辦例行記者會上，有媒體提問，台積電日前宣佈要在南京擴產28奈米全球製程產能帶，中芯國際日前也曾宣佈要在深圳合作擴產28奈米晶片製程，\
    #         中國有專家表示，台積電擴產或對中芯國際產生排擠競爭效應，還有學者呼籲中國應禁止台積電這個方案，請問對此有何評論？馬曉光則回應，「相信我們是法治國家，會依法辦事，依法依規來處理」。\
    #         他強調，關於台資台企來中國投資，有完備的法律、法規和管理機制，對於具體個案，有關部門會科學評估，依法依規處理。"
    ret_list = se.extract(text, keyword="詐騙", threshold=0.5)
    ret_list = se.extract(text)
    # print(ret_list)
