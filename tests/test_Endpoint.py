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

    def test_mandate_str(self):
        component = { 'type': 'str' }
        self.assertEqual(type(self.endpoint.mandate("hello, world", component)), str)
        self.assertEqual(type(self.endpoint.mandate(123, component)), str)
        self.assertEqual(type(self.endpoint.mandate(True, component)), str)

    def test_mandate_str_contains(self):
        component = {
            'type': 'str',
            'contains': [
                "hello",
                "world",
                "myke"
            ],
        }

        self.assertFalse(self.endpoint.mandate("hello, world", component))
        self.assertTrue(self.endpoint.mandate("myke says hello, world", component))

    def test_mandate_str_regex(self):
        component = {
            'type': 'str',
            're': [
                "^hello",
                "world$",
                "myke"
            ],
        }

        self.assertFalse( self.endpoint.mandate("hello, world", component) )
        self.assertTrue( self.endpoint.mandate("hello myke this is the world", component ) )



