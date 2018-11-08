#! $(env python)

import json

from flask import Flask
app = Flask(__name__)

sample = {
	"hello": "world", "hi": "hello"
}

with open("sample.json") as data:
	sample = json.load(data)

@app.route('/')
def root():
	return "{'hi': 'hello'}", 200,  {'Content-Type': 'application/json'}

@app.route("/<string:resource>")
def list(resource):
	return resource, 200, {'Content-Type': 'application/json'}

@app.route("/<string:resource>/<tag>")
def item(resource, tag):
	endpoint = sample[resource]
	return json.dumps(endpoint), 200, {'Content-Type': 'application/json'}
