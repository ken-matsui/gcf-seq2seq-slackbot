# coding: utf-8

import os
import glob
from datetime import datetime, timedelta

# from slackbot.bot import default_reply
from google.cloud import storage

from att_seq2seq.model import AttSeq2Seq
from att_seq2seq.decoder import Decoder
from converter import DataConverter


EMBED_SIZE = 100
HIDDEN_SIZE = 100
BATCH_SIZE = 20
BATCH_COL_SIZE = 15


# Instantiates a client
storage_client = storage.Client()

data_converter = DataConverter()
vocab_size = len(data_converter.vocab)
model = AttSeq2Seq(vocab_size=vocab_size,
                   embed_size=EMBED_SIZE,
                   hidden_size=HIDDEN_SIZE,
                   batch_col_size=BATCH_COL_SIZE)

# CloudStorageからmodelファイルをDownload
npz = '80.npz'
bucket = storage_client.get_bucket('model-files')  # rootとなるbucketを指定
blob = storage.Blob('chainer/att-seq2seq/v1/' + npz, bucket)  # rootから子を指定
with open('/tmp/' + npz, 'wb') as file_obj:  # localに保存するファイルを指定
    blob.download_to_file(file_obj)
decoder = Decoder(model, data_converter, '/tmp/' + npz)
os.remove('/tmp/' + npz)  # 使用後は消去


# @default_reply()
def default_func(msg):
    # "query: |->     "
    query = msg.text[7:]
    response = decoder(query)
    return response

