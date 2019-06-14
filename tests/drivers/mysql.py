#! /usr/bin/env python3

import importlib
import unittest

import yaml

from drivers.mysql import Driver

class DriverTestCase(unittest.TestCase):
	def setUp(self):
		self.creds = {
			'host': "127.0.0.1",
            		'user': "root",
			'passwd': "+zQx57?4$9",
        	}

		self.driver = Driver(creds)
		with open('./examples/data.yml') as f:
			self.data = yaml.load(f)

		
