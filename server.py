from flask import Flask, request, jsonify
from pymongo import MongoClient

mongoUrl = 'mongodb://localhost:27017/'

app = Flask(__name__)
client = MongoClient(mongoUrl)
sysinfo = client.info.sysinfo

@app.route('/', methods=['POST'])
def index():
	object_id = sysinfo.insert(request.json)
	return str(object_id)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6000)
