#! $(env python)

from jinja2 import Template

from MysqlDriver import Driver as mysql
from MongoDriver import Driver as mongo

class Endpoint():
	def __init__(self, params, data, driver):
		self.data = data
		self.params = params
		self.db = self.driver(driver)(params)

	def driver(self, key):
		return {
			'mongo': mongo,
			'mysql': mysql,
		}[ key ]

	def get(self):
		query = self.data['get'].get('query', {})
		self.results = self.db.get(query)

		return self.transform('get')

	def render(self, src):
		src = str(src)

		t = Template(src)
		return t.render(**self.params)

	def transform(self, method):
		transforms = self.data[method].get('transforms', {})

		for transform in transforms:
			op = transform.get('op', '')
	
			op = getattr(self, op, None)
			if op:
				self.results = op(transform)

		return self.results

	def limit(self, transform):
		try:
			limit = int( self.render(transform['limit'] ) )
			return self.results[:limit]
		except ValueError:
	  		pass

		return self.results
	  
	def pagify(self, transform):
		page = int(self.render(transform['page']))
		amount = int(self.render(transform['amount']))

		start = (amount * page) - amount
		end = start + amount
		return self.results[start:end]
