#! /usr/bin/env python3

from importers.integer import TypeImporter

import unittest

EXPECTED_VALUE = 13


class ImporterIntegerTestCase(unittest.TestCase):
    def test_integer_as_integer(self):
        source = 'unittest'
        rule = 'test_integer_as_integer'
        value = 13
        component = {'type': 'integer'}

        type_importer = TypeImporter(source, rule, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_integer_as_string(self):
        source = 'unittest'
        rule = 'test_integer_type'
        value = '13'
        component = {'type': 'integer'}

        type_importer = TypeImporter(source, rule, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

        value = '13thirteen'
        type_importer = TypeImporter(source, rule, value, component)
        self.assertFalse(type_importer.valid())

    def test_integer_reject(self):
        source = 'unittest'
        rule = 'test_integer_reject'
        value = '13'
        component = {'type': 'integer', 'reject': ['this == 13']}

        type_importer = TypeImporter(source, rule, value, component)
        self.assertFalse(type_importer.valid())
