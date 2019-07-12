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

    def render_create_table(self, table):
        return """
			CREATE TABLE IF NOT EXISTS {} (
				id int NOT NULL AUTO_INCREMENT,
				firstname VARCHAR(255),
				lastname VARCHAR(255),
				hobby VARCHAR(255),
				lucky_number INT,
				PRIMARY KEY (id)
			);
		""".format(table)

    def render_insert_query(self, table):
        return {
            'op':
            "INSERT INTO {} (firstname, lastname, hobby, lucky_number) VALUES (%s, %s, %s, %s);"
            .format(table),
            'params': [
                '{{ data.firstname }}', '{{ data.lastname }}',
                '{{ data.hobby }}', '{{ data.lucky_number }}'
            ]
        }

    def test_post(self):
        table = 'dude_tests.test_post_data'

        self.driver.cursor.execute(self.render_create_table(table))

        imported = {
            'cookies': {},
            'data': self.get_data(),
            'form': {},
            'header': {},
            'url': {},
        }

        query = self.render_insert_query(table)
        self.driver.post(imported, query)
