#! /usr/bin/env python3

import importlib
import unittest

import yaml

from drivers.mysql import Driver

class DriverTestCase(unittest.TestCase):
	def setUp(self):
		self.bank = {
			'host': "127.0.0.1",
			'user': "root",
			'passwd': "+zQx57?4$9",
		}

		self.driver = Driver(self.bank)

		self.driver.cursor.execute("CREATE DATABASE IF NOT EXISTS dude_tests;")


	def get_data(self):
		with open('./examples/tests/data.yml') as f:
			return yaml.load(f, Loader=yaml.Loader)


	def test_post(self):
		self.driver.cursor.execute("""
			CREATE TABLE IF NOT EXISTS dude_tests.test_post_data (
				id int NOT NULL AUTO_INCREMENT,
				firstname VARCHAR(255),
				lastname VARCHAR(255),
				hobby VARCHAR(255),
				lucky_number INT,
				PRIMARY KEY (id)
			);
		""")

		imported = {
			'cookies': {},
			'data': self.get_data(),
			'form': {},
			'header': {},
			'url': {},
		}

		query = {
			'op': "INSERT INTO dude_tests.test_post_data (firstname, lastname, hobby, lucky_number) VALUES (%s, %s, %s, %s);",
			'params': [
				'{{ data.firstname }}',
				'{{ data.lastname }}',
				'{{ data.hobby }}',
				'{{ data.lucky_number }}'
			]
		}
		query = self.driver.post(imported, query)

#		self.driver.cursor.execute("DROP TABLE dude_tests.test_post_data;")
