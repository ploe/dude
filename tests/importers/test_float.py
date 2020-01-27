#! /usr/bin/env python3
"""importers/float unittests module"""

import unittest

from importers.float import TypeImporter

EXPECTED_VALUE = 3.14159


class ImporterBooleanTestCase(unittest.TestCase):
    """importers/float TestCase"""
    def test_float_as_float(self):
        """unittest to ensure that a float can be coerced to a float"""
        source = 'unittest'
        tag = 'test_float_as_float'
        value = 3.14159
        component = {'type': 'float'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

    def test_float_as_string(self):
        """unittest to ensure that a string can be coerced to a float"""
        source = 'unittest'
        tag = 'test_float_type'
        value = "{}".format(EXPECTED_VALUE)
        component = {'type': 'float'}

        type_importer = TypeImporter(source, tag, value, component)
        self.assertTrue(type_importer.valid())
        self.assertTrue(type_importer.value, EXPECTED_VALUE)

        value = '3.14pi'
        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())

    def test_float_reject(self):
        """unittest to ensure that reject mechanism works - DEPRECATED"""
        source = 'unittest'
        tag = 'test_boolean_reject'
        value = EXPECTED_VALUE
        component = {
            'type': 'float',
            'reject': ["this == {}".format(EXPECTED_VALUE)]
        }

        type_importer = TypeImporter(source, tag, value, component)
        self.assertFalse(type_importer.valid())
