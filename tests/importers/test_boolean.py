#! /usr/bin/env python3

from importers.boolean import TypeImporter

import unittest

class ImporterBooleanTestCase(unittest.TestCase):
    def test_boolean_true(self):
        value = True
        component = {
            'type': 'boolean'
        }

        type_importer = TypeImporter(value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value)

    def test_boolean_false(self):
        value = False
        component = {
            'type': 'boolean'
        }

        type_importer = TypeImporter(value, component)
        self.assertTrue(type_importer.valid())
        self.assertFalse(type_importer.value)

    def test_boolean_reject(self):
        value = True
        component = {
            'type': 'boolean',
            'reject': ['this == True']
        }

        type_importer = TypeImporter(value, component)
        self.assertFalse(type_importer.valid())

    def test_boolean_as_false(self):
        value = 'False'
        component = {
            'type': 'boolean',
            'as_false': ['False']
        }

        type_importer = TypeImporter(value, component)
        self.assertFalse(type_importer.value)

