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

    def create_table(self, table):
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

    def drop_table(self, table):
        query = "DROP TABLE IF EXISTS {}".format(table)

        self.driver.cursor.execute(query)

    def get_imported_data(self):
        imported = {
            'cookies': {},
            'form': {
                'firstname': 'David',
                'lucky_number': 6
            },
            'header': {},
            'url': {},
        }

        with open('./examples/tests/data.yml') as f:
            imported['data'] = yaml.load(f, Loader=yaml.Loader)

        return imported

    def insert_query(self, imported, table):
        query = {
            'op':
            "INSERT INTO {} (firstname, lastname, hobby, lucky_number) VALUES (%s, %s, %s, %s);"
            .format(table),
            'params': [
                '{{ data.firstname }}', '{{ data.lastname }}',
                '{{ data.hobby }}', '{{ data.lucky_number }}'
            ]
        }

        self.driver.post(imported, query)

    def select_query(self, imported, table):
        query = {
            'op':
            "SELECT * FROM {} WHERE firstname=%s and lucky_number=%s ORDER BY id DESC"
            .format(table),
            'params': [
                '{{ form.firstname }}',
                '{{ form.lucky_number }}',
            ],
        }

        return self.driver.get(imported, query)

    def test_get(self):
        table = 'dude_tests.test_get_data'
        self.create_table(table)

        imported = self.get_imported_data()
        self.insert_query(imported, table)
        print(self.select_query(imported, table))

        self.drop_table(table)

    def test_post(self):
        table = 'dude_tests.test_post_data'
        self.create_table(table)

        imported = self.get_imported_data()

        query = self.insert_query(imported, table)

        self.drop_table(table)
