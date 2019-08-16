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

    def delete_table(self, table):
        query = "DROP TABLE IF EXISTS {}".format(table)
        self.driver.cursor.execute(query)

    def insert_into_table(self, table):
        imported = {'data': self.get_imported_data()}
        query = {
            'op':
            "INSERT INTO {} (firstname, lastname, hobby, lucky_number) VALUES (%s, %s, %s, %s);"
            .format(table),
            'params': [
                'data.firstname', 'data.lastname', 'data.hobby',
                'data.lucky_number'
            ]
        }
        return self.driver.post(imported, query)

    def select_table(self, table, firstname, lucky_number):
        imported = {
            'args': {
                'firstname': firstname,
                'lucky_number': lucky_number,
            }
        }
        query = {
            'op':
            "SELECT * FROM {} WHERE firstname=%s and lucky_number=%s ORDER BY id DESC"
            .format(table),
            'params': ['args.firstname', 'args.lucky_number'],
        }
        return self.driver.get(imported, query)

    def get_imported_data(self):
        with open('./examples/tests/data.yml') as f:
            return yaml.load(f, Loader=yaml.Loader)

    def test_delete(self):
        table = 'dude_unittests.test_delete'
        self.delete_table(table)
        self.create_table(table)

        firstname = 'George'

        rows = self.insert_into_table(table)
        data = []
        for row in rows:
            if row['firstname'] != firstname:
                for key in ('created', 'dob'):
                    row.pop(key)
                row['id'] = row.pop('lastrowid')
                data.append(row)

        imported = {'data': [], 'form': {'firstname': firstname}}
        query = {
            'op': "DELETE FROM {} WHERE firstname=%s".format(table),
            'params': ['form.firstname']
        }

        self.driver.delete(imported, query)

        imported = {}
        query = {'op': "SELECT * FROM {} ORDER BY id DESC".format(table)}
        selects = self.driver.get(imported, query)

        for select in selects:
            datum = data.pop()

            for key in datum:
                self.assertEqual(select[key], datum[key])

    def test_get(self):
        table = 'dude_unittests.test_get'
        self.delete_table(table)
        self.create_table(table)

        inserts = self.insert_into_table(table)

        firstname = 'Noah'
        lucky_number = 7

        data = []
        for insert in inserts:
            if (insert['firstname'] == firstname) and (
                    insert['lucky_number'] == lucky_number):
                insert['id'] = insert.pop('lastrowid')
                data.append(insert)

        rows = self.select_table(table, firstname, lucky_number)

        for row in rows:
            datum = data.pop()

            for key in row:
                self.assertEqual(row[key], datum[key])

    def test_patch(self):
        table = 'dude_unittests.test_patch'
        self.delete_table(table)
        self.create_table(table)

    def test_post(self):
        table = 'dude_unittests.test_post'
        self.delete_table(table)
        self.create_table(table)

        rows = self.insert_into_table(table)

        for row in rows:
            self.assertTrue(row.get('lastrowid', False))
