# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Check if Word2Vec model is in local dir when import src.KeyGenerator

import os
import tarfile

import gdown

ROOTDIR = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
MODELPATH = os.path.join(ROOTDIR, "model", "word2vec")
FILEPATH = os.path.join(MODELPATH, "20210603040434-fast.tar.gz")  # 1.05GB

if not os.path.exists(MODELPATH):
    os.makedirs(MODELPATH)

    id = "1B0Vqsl5YyIJIvaCy1_iuxhgaochcaas5"
    url = f"https://drive.google.com/uc?export=download&id={id}"
    gdown.download(url, FILEPATH)
    tar = tarfile.open(FILEPATH, "r:gz")
    tar.extractall(MODELPATH)
    os.remove(FILEPATH)
