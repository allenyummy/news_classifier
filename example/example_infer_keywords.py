# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Example code for generating words

from datetime import datetime

from src.KeyGenerator.KeyGenerator import Word2VecKeyGenerator

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
nn_outfile_txt = f"src/utils/keywords/negative_news/NN_keywords_{now}.txt"
w2v.infer(nn_file, topn, threshold, force_info=None, init_results=True)
w2v.save2json(outfile=nn_outfile_json)
w2v.save2txt(outfile=nn_outfile_txt)

""" ESG """
now = datetime.now().strftime("%Y%m%d%H%M%S")
esg_file = "src/utils/keywords/esg_news/ESG_keywords.txt"
esg_outfile_json = f"src/utils/keywords/esg_news/ESG_keywords_{now}.json"
esg_outfile_txt = f"src/utils/keywords/esg_news/ESG_keywords_{now}.txt"
w2v.infer(esg_file, topn, threshold, force_info=None, init_results=True)
w2v.save2json(outfile=esg_outfile_json)
w2v.save2txt(outfile=esg_outfile_txt)
