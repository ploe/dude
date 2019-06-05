#! /usr/bin/env python3

import unittest

from Endpoint import Endpoint

class EndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.endpoint = Endpoint('tests/endpoints/test_Endpoint.yml')

    def test_init(self):
        self.assertTrue(self.endpoint)

    def test_create(self):
        client = {}
        output = self.endpoint.run_pipeline_until(client, "CREATE", "test_create")

    def test_import_str(self):
        component = { 'type': 'str' }
        self.assertEqual(type(self.endpoint.import("hello, world", component)), str)
        self.assertEqual(type(self.endpoint.import(123, component)), str)
        self.assertEqual(type(self.endpoint.import(True, component)), str)

    def test_import_str_contains(self):
        component = {
            'type': 'str',
            'contains': {
                'op': 'accept',
                'values': [
                    'hello',
                    'world',
                    'spam'
                ]
            },
        }

        self.assertFalse(self.endpoint.import("hello, world", component))
        self.assertTrue(self.endpoint.import("spam says hello, world", component))

    def test_import_str_regex(self):
        component = {
            'type': 'str',
            're': [
                "^hello",
                "world$",
                "spam"
            ],
        }

        self.assertFalse( self.endpoint.import("hello, world", component) )
        self.assertTrue( self.endpoint.import("hello spam this is the world", component ) )

    def test_import_str_deny(self):
        component = {
            'type': 'str',
            'deny': [
                "'hello' in this",
                "this | length <= 5"
            ],
        }

        self.assertFalse( self.endpoint.import("world", component) )
        self.assertFalse( self.endpoint.import("hello, world", component) )
        self.assertTrue( self.endpoint.import("spam eggs spam", component) )

    def test_import_str_validate_contains(self):
        component = {
            'type': 'str',
            'contains': {
                'op': 'accept',
                'values': 'spam',
            }
        }

        self.assertTrue( self.endpoint.validate_component(component) )
