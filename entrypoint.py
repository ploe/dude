#! /usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.before_first_request
def before_first_request():
	# dir = get env(DUDE_DOMAIN_DIR)
	# domain = Domain(dir)
	print("load endpoints")


@app.route('/status')
def status():
	return 'up!'

@app.route('/<path:path>', methods=['DELETE', 'GET', 'POST', 'PATCH'])
def endpoint(path):
	print("get endpoint")
	# endpoint = domain.get(path)
	# vars = Importer(request)
	print("vars = import values")
	# data = Driver(endpoint, vars)
	print("data = query driver")
	# response = Transform(endpoint, vars)
	print("response = transformed data")
	return 'Hello, World!'
