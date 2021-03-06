#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import AutoReconnect

if os.getenv('BAE_ENV_APPID'):
	db_username = os.getenv('BAE_USER_AK')
	db_password = os.getenv('BAE_USER_SK')
	db_host = os.getenv('BAE_MONGODB_HOST')
	db_port = os.getenv('BAE_MONGODB_PORT')
	db_name = os.getenv('BAE_MONGODB_NAME')
	db_collection = 'sysinfo'
	mongoUrl = "mongodb://{}:{}@{}:{}/{}".format(db_username, db_password, db_host, db_port, db_name)
else:
	db_host = 'localhost'
	db_name = 'sysinfo'
	db_collection = 'sysinfo'
	mongoUrl = "mongodb://{}/{}".format(db_host, db_name)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	sysinfo = MongoClient(mongoUrl)[db_name][db_collection]
	info = request.json
	info['remoteip'] = request.remote_addr
	object_id = sysinfo.insert(info)
	return str(object_id)

if os.getenv('BAE_ENV_APPID'):
	from bae.core.wsgi import WSGIApplication
	application = WSGIApplication(app)
else:
	app.run(host='0.0.0.0', port=os.getenv('PORT', 8000))
