#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import time
from functools import wraps
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
sysinfo = MongoClient(mongoUrl)[db_name][db_collection]

def reconnect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 2
        num_fails = 0
        while True:
            try:
                return func(*args, **kwargs)
            except AutoReconnect as e:
                num_fails += 1
                time.sleep(0.1)
                if num_fails >= max_retries:
                    raise e
    return wrapper

@app.route('/', methods=['POST'])
@reconnect
def index():
	object_id = sysinfo.insert(request.json)
	return str(object_id)

if os.getenv('BAE_ENV_APPID'):
	from bae.core.wsgi import WSGIApplication
	application = WSGIApplication(app)
else:
	app.run(host='0.0.0.0', port=os.getenv('PORT', 8000))
