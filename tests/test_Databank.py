#! /usr/bin/env python3

import unittest
from time import sleep

from Databank import Databank

class DatabankTestCase(unittest.TestCase):
    def setUp(self):
        self.databank = Databank("tests/banks/test_Databank.yml")


    def test_init(self):
        self.assertTrue(self.databank)
        self.assertEqual(self.databank.data['driver'], "MySQL")
        self.assertTrue(self.databank.data['login'])


    def test_connect(self):
        driver = self.databank.connect()
        self.assertTrue(driver)

       
