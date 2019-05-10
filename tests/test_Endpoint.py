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

