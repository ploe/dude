import unittest

from Databank import Databank

class DatabankTestCase(unittest.TestCase):
    def setUp(self):
        self.databank = Databank("databanks/test_Databank.yml")

    def test_init(self):
        self.assertTrue(self.databank)
        self.assertEqual(self.databank.data['driver'], "MySQL")
        self.assertTrue(self.databank.data['login'])

    def test_connect(self):
        driver = self.databank.connect()
        self.assertTrue(driver)
        
