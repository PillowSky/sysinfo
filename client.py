#!/usr/bin/python

import os
import re
import socket
import json
import urllib2
import datetime
import flask

url = 'http://localhost:6000'
label = 'Aspire'

sysinfo = {}

# label
sysinfo['label'] = label

#uptime
with open('/proc/uptime', 'r') as f:
	sysinfo['uptime'] = str(datetime.timedelta(seconds = float(f.readline().split()[0])))

#localip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.duapp.com', 80))
sysinfo['localip'] = s.getsockname()[0]
s.close()

#cpuinfo
with open('/proc/cpuinfo', 'r') as f:
	info = f.read()
	sysinfo['cpuinfo'] = {
		'model': re.search(r'model name.*:\s(.*)', info).groups()[0],
		'count': info.count('processor')
	}

#meminfo
with open('/proc/meminfo', 'r') as f:
	info = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
	sysinfo['meminfo'] = {
		'MemTotal': info.get('MemTotal'),
		'MemFree': info.get('MemFree'),
		'MemAvailable': info.get('MemAvailable'),
		'Buffers': info.get('Buffers'),
		'Cached': info.get('Cached')
	}

#loadavg
sysinfo['loadavg'] = os.getloadavg()[2]

# all done, make log
print(sysinfo)

# send to server
object_id = urllib2.urlopen(urllib2.Request(url, json.dumps(sysinfo), {'Content-Type': 'application/json'})).read()
print(object_id)

# define wsgi application
app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return flask.jsonify(sysinfo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)