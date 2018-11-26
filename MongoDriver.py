#! $(env python)

from pymongo import MongoClient

from BaseDriver import BaseDriver

class Driver(BaseDriver):
	def __init__(self, params):
		self.client = MongoClient()
		self.params = params

	def get(self, query):
		collection = self.client[ query['db'] ][ query['collection'] ]

		output = []
		for member in collection.find( query['op'] ):
			member['_id'] = str( member['_id'] )
			output.append(member)

		return output


