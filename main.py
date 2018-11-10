#! $(env python)

import json

from flask import Flask
app = Flask(__name__)

import MySQLdb

sample = {
	"hello": "world", "hi": "hello"
}

class MysqlDriver():
	def __init__(self):
		self.db = MySQLdb.connect(
  			host="localhost",
 			user="root",
  			passwd="+zQx57?4$9",
  			db="crud"
		)

		self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

	def __del__(self):
		self.db.close()

	def query(self, op, params):
		self.cursor.execute(op, params)
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
	db = MysqlDriver()

	endpoint = sample[resource]

	query = endpoint['item']['get']['query']
	print(query)
	item = db.query(query['op'], (52,))

	return json.dumps(item), 200, {'Content-Type': 'application/json'}
