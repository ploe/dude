#! $(env python)

import json

from flask import Flask, request, g
app = Flask(__name__)

from jinja2 import Template

import MySQLdb

sample = {
	"hello": "world", "hi": "hello"
}

class MysqlDriver():
	def __init__(self, uri, url):
		self.db = MySQLdb.connect(
  			host="localhost",
 			user="root",
  			passwd="+zQx57?4$9",
  			db="crud"
		)

		self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
		self.uri = uri
		self.url = url

	def __del__(self):
		self.db.close()

	def jinja(self, param):
		t = Template(param)
		return t.render(uri=self.uri, url=self.url)

	def query(self, query):
		params = []
		for param in query['params']:
			params.append( self.jinja(param) )

		self.cursor.execute(query['op'], params)
		return self.cursor.fetchall()

with open("sample.json") as data:
	sample = json.load(data)

def ok(output):
	return respond(output, 200)

def respond(output, code):
	return json.dumps(output), 200, {'Content-Type': 'application/json'}

@app.before_request
def before_request():
	url = {}
	for key, value in request.args.iteritems():
		url[key] = value

	g.url = url
	
@app.route('/')
def root():
	return "{'hi': 'hello'}", 200,  {'Content-Type': 'application/json'}

@app.route("/<string:resource>", strict_slashes=False)
def list(resource):
	return resource, 200, {'Content-Type': 'application/json'}

@app.route("/<string:resource>/<string:tag>", strict_slashes=False)
def item(resource, tag):
	db = MysqlDriver({ 'resource': resource, 'tag': tag }, g.url)

	endpoint = sample[resource]['item']['get']

	query = endpoint['query']
	item = db.query(query)

	if len(item) != 1:
		abort(500)

	this = item[0]

	data = endpoint['data']
	types = endpoint['types']

	output = {}
	for key, value in data.iteritems():
		t = Template(value)
		output[key] = t.render(this=this)
	
	return ok(output)

@app.errorhandler(404)
def not_found(error):
    return respond({'error': request.base_url}, 404)

@app.errorhandler(500)
def internal_error(error):
    return respond({'error': 'internal server error'}, 500)
