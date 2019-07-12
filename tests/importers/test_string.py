#! /usr/bin/env python3

from importers.string import TypeImporter

import unittest

EXPECTED_VALUE = 'hello, world'


class ImporterStringTestCase(unittest.TestCase):
    def test_string_as_string(self):
        key = 'unittest'
        rule = 'test_string_as_string'
        value = 'hello'
        component = {'type': 'string'}

        type_importer = TypeImporter(key, rule, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_string_as_integer(self):
        key = 'unittest'
        rule = 'test_string_type'
        value = 13
        component = {'type': 'string'}

        type_importer = TypeImporter(key, rule, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_string_reject(self):
        key = 'unittest'
        rule = 'test_string_reject'
        value = EXPECTED_VALUE
        component = {'type': 'string', 'reject': ['this == "hello, world"']}

        type_importer = TypeImporter(key, rule, value, component)
        self.assertFalse(type_importer.valid())
