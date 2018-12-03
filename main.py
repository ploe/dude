#! $(env python)

import json
from glob import glob

from flask import abort, Flask, g, jsonify, request
app = Flask(__name__)
from jinja2 import Template

from Endpoint import Endpoint

domain = {}
for c in glob('*.json'):
	with open(c) as data:
		sample = json.load(data)
		domain[sample['name']] = sample

def respond_ok(output):
	return respond(output, 200)

def respond(output, code):
	return jsonify(output), code, {'Content-Type': 'application/json'}

def render_member(this, endpoint):
	data = endpoint['data']
	types = endpoint.get('types', {})

	output = {}
	for key, src in data.iteritems():
		value = render(src, {'this': this})
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
	params = {
		'uri': { 'collection': collection },
		'url': g.url,
	}

	driver = domain[collection]['driver']
	endpoint = Endpoint( 
		params, 
		domain[collection]['collection'],
		driver,
	)

	output = endpoint.get()	
	return respond_ok(output)

@app.route("/<string:collection>/<string:member>", methods=['GET'], strict_slashes=False)
def member_get(collection, member):
	db = mysql({ 'collection': collection, 'member': member }, g.url)

	endpoint = domain[collection]['member']['get']

	query = endpoint['query']
	results = db.member_get(query)

	if len(results) > 1:
		abort(500)

	this = results[0]

	output = render_member(this, endpoint)
	
	return respond_ok(output)

@app.route("/<string:collection>", methods=['POST'], strict_slashes=False)
def collection_post(collection):
	db = mysql({ 'collection': collection }, g.url)

	endpoint = domain[collection]['collection']['post']

	query = endpoint['query']
	db.collection_post(query)

	return respond_ok({'posted': True})

@app.errorhandler(404)
def not_found(error):
	return respond({'error': request.base_url }, 404)

@app.errorhandler(500)
def internal_error(error):
	return respond({'error': 'internal server error'}, 500)
