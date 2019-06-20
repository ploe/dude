#! /usr/bin/env python3

from importers.base import TypeImporter as base

class TypeImporter(base):
	def init_type_importer(self, component):
		self.type = 'integer'
		self.load_component(component, [], 'reject')

		self.value_to_integer()

	def value_to_integer(self):
		try:
			self.value = int(self.value)
		except ValueError:
			err = "{}['{}'] ({}): invalid integer".format(
				self.key,
				self.rule, 
				self.type, 
				self.value)

			self.errors.append(err)

		return self.has_errors()


	def valid(self):
		self.validate_reject()
		return not self.has_errors()
