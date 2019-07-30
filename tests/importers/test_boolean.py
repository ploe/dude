#! /usr/bin/env python3

from importers.boolean import TypeImporter

import unittest


class ImporterBooleanTestCase(unittest.TestCase):
    def test_boolean_true(self):
        source = 'unittest'
        tag = 'test_boolean_true'
        value = True
        component = {'type': 'boolean'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value)

    def test_boolean_false(self):
        source = 'unittest'
        tag = 'test_boolean_false'
        value = False
        component = {'type': 'boolean'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertFalse(type_importer.value)

    def test_boolean_reject(self):
        source = 'unittest'
        tag = 'test_boolean_reject'
        value = True
        component = {'type': 'boolean', 'reject': ['this == True']}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())

    def test_boolean_as_false(self):
        source = 'unittest'
        tag = 'test_boolean_as_false'
        value = 'False'
        component = {'type': 'boolean', 'as_false': ['False']}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.value)
