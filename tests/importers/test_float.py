#! /usr/bin/env python3

from importers.float import TypeImporter

import unittest

EXPECTED_VALUE = 3.14159


class ImporterBooleanTestCase(unittest.TestCase):
    def test_float_as_float(self):
        source = 'unittest'
        rule = 'test_float_as_float'
        value = 3.14159
        component = {'type': 'float'}

        type_importer = TypeImporter(source, rule, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_float_as_string(self):
        source = 'unittest'
        rule = 'test_float_type'
        value = "{}".format(EXPECTED_VALUE)
        component = {'type': 'float'}

        type_importer = TypeImporter(source, rule, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

        value = '3.14pi'
        type_importer = TypeImporter(source, rule, value, component)
        self.assertFalse(type_importer.valid())

    def test_float_reject(self):
        source = 'unittest'
        rule = 'test_boolean_reject'
        value = EXPECTED_VALUE
        component = {
            'type': 'float',
            'reject': ["this == {}".format(EXPECTED_VALUE)]
        }

        type_importer = TypeImporter(source, rule, value, component)
        self.assertFalse(type_importer.valid())
