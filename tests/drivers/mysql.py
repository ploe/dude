#! /usr/bin/env python3

import importlib
import unittest

import yaml

from drivers.mysql import Driver

class DriverTestCase(unittest.TestCase):
    def setUp(self):
        self.src = {
            'host': "127.0.0.1",
            'user': "root",
            'passwd': "+zQx57?4$9",
        }

        self.driver = Driver(self.src)

        self.driver.cursor.execute("""
            CREATE DATABASE dude;
            CREATE TABLE dude.test_MySQLDriver (
                id int NOT NULL AUTO_INCREMENT,
                dob DATE,
                firstname VARCHAR(255),
                lucky_number INT,
                PRIMARY KEY (id)
            );
        """)

#    def tearDown(self):
#        self.driver.cursor.execute("DROP DATABASE dude")
#
#    def test_init(self):
#       self.assertTrue(self.driver)

    def test_create(self):
        data = self.get_data()
        query = self.get_query(data)

        self.assertTrue(self.driver.create(query))

    def get_data(self):
        with open('./examples/tests/data.yml') as f:
            return yaml.load(f, Loader=yaml.Loader)

    def get_query(self, data):
        imported = {
            'cookies': {},
            'data': data,
            'header': {},
            'url': {}
        }

        query = {
            'op': "INSERT INTO dude.test_MySQLDriver (dob, firstname, lucky_number) VALUES (%s, %s, %s);",
            'params': []
        }

        for row in data:
            query['params'].append([
                row['dob'],
                row['firstname'],
                row['lucky_number']
            ])

        return query
