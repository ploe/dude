#! /usr/bin/env python3
"""importers/string unittests module"""

import unittest

from importers.string import TypeImporter

EXPECTED_VALUE = 'hello, world'


class ImporterStringTestCase(unittest.TestCase):
    """importers/string TestCase"""
    def test_string_as_string(self):
        """unittest to ensure that a string can be coerced to a string"""
        source = 'unittest'
        tag = 'test_string_as_string'
        value = 'hello'
        component = {'type': 'string'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_string_as_integer(self):
        """unittest to ensure that an integer can be coerced to a string"""
        source = 'unittest'
        tag = 'test_string_type'
        value = 13
        component = {'type': 'string'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_string_reject(self):
        """unittest to ensure that reject mechanism works - DEPRECATED"""
        source = 'unittest'
        tag = 'test_string_reject'
        value = EXPECTED_VALUE
        component = {'type': 'string', 'reject': ['this == "hello, world"']}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())
