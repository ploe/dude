#! $(env python)

from pymongo import MongoClient

from BaseDriver import BaseDriver

class Driver(BaseDriver):
	def __init__(self, params):
		self.db = MongoClient()
		self.params = params

	def get(self, query):
		return []
