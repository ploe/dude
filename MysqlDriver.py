#! $(env python)

from jinja2 import Template

import MySQLdb

from BaseDriver import BaseDriver

class Driver(BaseDriver):
	def __init__(self, params):
		self.db = MySQLdb.connect(
  			host="localhost",
 			user="root",
  			passwd="+zQx57?4$9",
  			db="crud"
		)

		self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
		self.uri = params['uri']
		self.url = params['url']

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

	def get(self, query):
		return self.read(query)

	def member_get(self, query):
		return self.read(query)

	def collection_get(self, query):
		return self.read(query)

	def collection_post(self, query):
		params = self.jinja_params(query)

		self.cursor.execute(query['op'], params)
		self.db.commit()

		return True

