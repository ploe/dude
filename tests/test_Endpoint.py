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

    def test_mandate(self):
        component = { 'type': 'str' }
        self.assertEqual(type(self.endpoint.mandate("hello, world", component)), str)
        self.assertEqual(type(self.endpoint.mandate(123, component)), str)
        self.assertEqual(type(self.endpoint.mandate(True, component)), str)

