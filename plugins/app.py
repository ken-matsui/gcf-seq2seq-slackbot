# coding: utf-8

import os
import glob
from datetime import datetime, timedelta

from slackbot.bot import default_reply
from google.cloud import datastore
from google.cloud import storage

from att_seq2seq.model import AttSeq2Seq
from att_seq2seq.decoder import Decoder
from converter import DataConverter


EMBED_SIZE = 100
HIDDEN_SIZE = 100
BATCH_SIZE = 20
BATCH_COL_SIZE = 15


# Instantiates a client
datastore_client = datastore.Client()
storage_client = storage.Client()

data_converter = DataConverter()
vocab_size = len(data_converter.vocab)
model = AttSeq2Seq(vocab_size=vocab_size,
				   embed_size=EMBED_SIZE,
				   hidden_size=HIDDEN_SIZE,
				   batch_col_size=BATCH_COL_SIZE)

# CloudStorageからmodelファイルをDownload
npz = '80.npz'
bucket = storage_client.get_bucket('model-files') # rootとなるbucketを指定
blob = storage.Blob('chainer/att-seq2seq/v1/' + npz, bucket) # rootから子を指定
with open('./' + npz, 'wb') as file_obj: # localに保存するファイルを指定
	blob.download_to_file(file_obj)
decoder = Decoder(model, data_converter, './' + npz)
os.remove('./' + npz) # 使用後は消去


@default_reply()
def default_func(message):
	query = message.body['text']
	response = decoder(query)
	message.reply(response)
	username = message.channel._client.users[message.body['user']][u'name']
	store_data(int(float(message.body['ts'])), username, query, response)

def store_data(timestamp, user, query, response):
	# The kind for the new entity
	kind = 'Talk'
	# The name/ID for the new entity
	time = datetime.fromtimestamp(timestamp)
	time += timedelta(hours=9) # timezoneをJSTに調整
	name = str(time)
	# The Cloud Datastore key for the new entity
	talk_key = datastore_client.key(kind, name)

	# Prepares the new entity
	talk = datastore.Entity(key=talk_key)
	talk['1.TimeStamp'] = timestamp
	talk['2.User'] = user
	talk['3.Query'] = query
	talk['4.Response'] = response

	# Saves the entity
	datastore_client.put(talk)