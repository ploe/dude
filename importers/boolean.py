#! /usr/bin/env python3

from importers.base import TypeImporter as base

class TypeImporter(base):
	def init_type_importer(self, component):
		self.type = 'boolean'
		self.load_component(component, [], 
			'reject',
			'as_false')

		self.value = self.value_as_false()


	def valid(self):
		return self.validate_reject()


	def value_as_false(self):
		for value in self.as_false:
			if self.value == value: return False

		return self.value


