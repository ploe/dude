#! /usr/bin/env python3

from importers.integer import TypeImporter

import unittest

EXPECTED_VALUE=13

class ImporterBooleanTestCase(unittest.TestCase):
	def test_integer_as_integer(self):
			key = 'unittest'
			rule = 'test_integer_as_integer'
			value = 13
			component = {
				'type': 'integer'
			}

			type_importer = TypeImporter(key, rule, value, component)
			self.assertTrue(type_importer.valid())
			self.assertTrue(type_importer.value, EXPECTED_VALUE)


	def test_integer_as_string(self):
			key = 'unittest'
			rule = 'test_integer_type'
			value = '13'
			component = {
				'type': 'integer'
			}

			type_importer = TypeImporter(key, rule, value, component)
			self.assertTrue(type_importer.valid())
			self.assertTrue(type_importer.value, EXPECTED_VALUE)

			value = '13thirteen'
			type_importer = TypeImporter(key, rule, value, component)
			self.assertFalse(type_importer.valid())


