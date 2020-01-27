#! /usr/bin/env python3
"""importers/integer unittests module"""

import unittest

from importers.integer import TypeImporter

EXPECTED_VALUE = 13


class ImporterIntegerTestCase(unittest.TestCase):
    """importers/integer TestCase"""
    def test_integer_as_integer(self):
        """unittest to ensure that an integer can be coerced to an integer"""
        source = 'unittest'
        tag = 'test_integer_as_integer'
        value = 13
        component = {'type': 'integer'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_integer_as_string(self):
        """unittest to ensure that a string can be coerced to an integer"""
        source = 'unittest'
        tag = 'test_integer_type'
        value = '13'
        component = {'type': 'integer'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

        value = '13thirteen'
        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())

    def test_integer_reject(self):
        """unittest to ensure that reject mechanism works - DEPRECATED"""

        source = 'unittest'
        tag = 'test_integer_reject'
        value = '13'
        component = {'type': 'integer', 'reject': ['this == 13']}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())
