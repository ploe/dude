#! /usr/bin/env python3
"""importers/boolean unittests module"""

import unittest

from importers.boolean import TypeImporter


class ImporterBooleanTestCase(unittest.TestCase):
    """importers/boolean TestCase"""
    def test_boolean_true(self):
        """unittest to ensure boolean True can be parsed"""
        source = 'unittest'
        tag = 'test_boolean_true'
        value = True
        component = {'type': 'boolean'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value)

    def test_boolean_false(self):
        """unittest to ensure boolean False can be parsed"""
        source = 'unittest'
        tag = 'test_boolean_false'
        value = False
        component = {'type': 'boolean'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertFalse(type_importer.value)

    def test_boolean_reject(self):
        """unittest to ensure the reject mechanism works - DEPRECATED"""
        source = 'unittest'
        tag = 'test_boolean_reject'
        value = True
        component = {'type': 'boolean', 'reject': ['this == True']}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())

    def test_boolean_as_false(self):
        """unittest to ensure the as_false mechanism works"""
        source = 'unittest'
        tag = 'test_boolean_as_false'
        value = 'False'
        component = {'type': 'boolean', 'as_false': ['False']}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.value)
