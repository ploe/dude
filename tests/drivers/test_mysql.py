#! /usr/bin/env python3

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

        self.driver.cursor.execute(
            "CREATE DATABASE IF NOT EXISTS dude_unittests;")

    def get_imported_data(self):
        with open('./examples/tests/data.yml') as f:
            return yaml.load(f, Loader=yaml.Loader)

    def test_post(self):
        table = 'dude_unittests.test_post'
        schema = """
            CREATE TABLE IF NOT EXISTS {} (
                id int NOT NULL AUTO_INCREMENT,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                hobby VARCHAR(255),
                lucky_number INT,
                PRIMARY KEY (id)
            );
        """.format(table)
        self.driver.cursor.execute(schema)

        imported = {'data': self.get_imported_data()}

        query = {
            'op':
            "INSERT INTO {} (firstname, lastname, hobby, lucky_number) VALUES (%s, %s, %s, %s);"
            .format(table),
            'params': [
                '{{ data.firstname }}', '{{ data.lastname }}',
                '{{ data.hobby }}', '{{ data.lucky_number }}'
            ]
        }
        rows = self.driver.post(imported, query)

        query = "DROP TABLE IF EXISTS {}".format(table)
        self.driver.cursor.execute(query)

        for row in rows:
            self.assertTrue(row.get('lastrowid', False))
