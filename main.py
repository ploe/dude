#! $(env python)

import json

from flask import Flask
app = Flask(__name__)

from jinja2 import Template

import MySQLdb

sample = {
	"hello": "world", "hi": "hello"
}

class MysqlDriver():
	def __init__(self, uri):
		self.db = MySQLdb.connect(
  			host="localhost",
 			user="root",
  			passwd="+zQx57?4$9",
  			db="crud"
		)

		self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
		self.uri = uri

	def __del__(self):
		self.db.close()

	def query(self, query):
		params = []
		for param in query['params']:
			t = Template(param)
			params.append(t.render(uri=self.uri))

		self.cursor.execute(query['op'], params)
		return self.cursor.fetchall()


with open("sample.json") as data:
	sample = json.load(data)

@app.route('/')
def root():
	return "{'hi': 'hello'}", 200,  {'Content-Type': 'application/json'}

@app.route("/<string:resource>")
def list(resource):
	return resource, 200, {'Content-Type': 'application/json'}

@app.route("/<string:resource>/<string:tag>")
def item(resource, tag):
	db = MysqlDriver({ 'resource': resource, 'tag': tag })

	endpoint = sample[resource]

	query = endpoint['item']['get']['query']
	item = db.query(query)

	return json.dumps(item), 200, {'Content-Type': 'application/json'}
