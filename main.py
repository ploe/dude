#! $(env python)

import json

from flask import abort, Flask, g, jsonify, request
app = Flask(__name__)

from jinja2 import Template

import MySQLdb

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
		self.cursor.close()
		self.db.close()

	def read(self, query):
		params = self.jinja_params(query)

		self.cursor.execute(query['op'], params)
		return self.cursor.fetchall()

	def write(self, query):
		params = self.jinja_params(query)

		self.cursor.execute(query['op'], params)
		self.db.commit()

		return True

	def jinja(self, param):
		t = Template(param)
		return t.render(uri=self.uri, url=self.url)

	def jinja_params(self, query):
		src = query.get('params', None)

		params = []
		if src != None:
			for param in src:
				params.append( self.jinja(param) )

		return params

	def member_get(self, query):
		return self.read(query)

	def collection_get(self, query):
		return self.read(query)

	def collection_post(self, query):
		params = self.jinja_params(query)

		self.cursor.execute(query['op'], params)
		self.db.commit()

		return True

domain = {}
with open("sample.json") as data:
	sample = json.load(data)
	domain[sample['name']] = sample

def ok(output):
	return respond(output, 200)

def respond(output, code):
	return jsonify(output), code, {'Content-Type': 'application/json'}

def render_member(this, endpoint):
	data = endpoint['data']
	types = endpoint.get('types', {})

	output = {}
	for key, raw in data.iteritems():
		t = Template(raw)
		value = t.render(this=this)
		convert = types.get(key, '')

		if convert == 'boolean':
			output[key] = bool(value)
		elif convert == 'integer':
			output[key] = int(value)
		elif convert == 'number':
			output[key] = float(value)
		else:
			output[key] = value
	return output

@app.before_request
def before_request():
	url = {}
	for key, value in request.args.iteritems():
		url[key] = value

	g.url = url

@app.route('/')
def root():
	return "{'hi': 'hello'}", 200,  {'Content-Type': 'application/json'}

@app.route("/<string:collection>", methods=['GET'], strict_slashes=False)
def collection_get(collection): 
	db = MysqlDriver({ 'collection': collection }, g.url)
	endpoint = domain[collection]['collection']['get']

	results = db.collection_get(endpoint['query'])

	output = []
	for this in results:
		output.append( render_member(this, endpoint) )

	transforms = endpoint.get('transforms', [])
	for transform in transforms:
		op = transform.get('op', '')

		value = None
		if op in ('limit', 'sort'):
			t = Template(transform[op])
			value = t.render(url=g.url)

		if op == 'limit':
			try:
				limit = int(value)
				output = output[:limit]

			except ValueError:
				pass
	
	return ok(output)

@app.route("/<string:collection>/<string:member>", methods=['GET'], strict_slashes=False)
def member_get(collection, member):
	db = MysqlDriver({ 'collection': collection, 'member': member }, g.url)

	endpoint = domain[collection]['member']['get']

	query = endpoint['query']
	results = db.member_get(query)

	if len(results) > 1:
		abort(500)

	this = results[0]

	output = render_member(this, endpoint)
	
	return ok(output)

@app.route("/<string:collection>", methods=['POST'], strict_slashes=False)
def collection_post(collection):
	db = MysqlDriver({ 'collection': collection }, g.url)

	endpoint = domain[collection]['collection']['post']

	query = endpoint['query']
	db.collection_post(query)

	return ok({'posted': True})

@app.errorhandler(404)
def not_found(error):
    return respond({'error': request.base_url }, 404)

@app.errorhandler(500)
def internal_error(error):
    return respond({'error': 'internal server error'}, 500)
