#! /usr/bin/env python3
"""drivers/mysql unittests module"""

import unittest

import yaml

from drivers.mysql import Driver


class DriverTestCase(unittest.TestCase):
    """drivers/mysql TestCase"""
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
        """CREATE TABLE query for unittests"""
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
        """DROP TABLE query for unittests"""
        query = "DROP TABLE IF EXISTS {}".format(table)
        self.driver.cursor.execute(query)

    def insert_into_table(self, table):
        """INSERT INTO query for unittests"""
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
        """SELECT query for unittests"""
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

    @staticmethod
    def get_imported_data():
        """get the example data for unittests"""
        with open('./examples/tests/data.yml') as file:
            return yaml.load(file, Loader=yaml.Loader)

    def test_delete(self):
        """DELETE unittest"""
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
        """GET unittest"""
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
        """PATCH unittest"""
        table = 'dude_unittests.test_patch'
        self.delete_table(table)
        self.create_table(table)

        rows = self.insert_into_table(table)

        firstname = "Myke"

        data = []
        for row in rows:
            for key in ('created', 'dob'):
                row.pop(key)

            row['id'] = row.pop('lastrowid')

            if row['firstname'] == firstname:
                row['hobby'] = 'Unit Testing'
                data.append(row)

        imported = {'data': data}
        query = {
            'op': "UPDATE {} SET hobby=%s WHERE id=%s".format(table),
            'params': ['data.hobby', 'data.id']
        }

        patched = self.driver.patch(imported, query)

        for patch in patched:
            self.assertEqual(patch.get('rowcount', 0), 1)

    def test_post(self):
        """POST unittest"""
        table = 'dude_unittests.test_post'
        self.delete_table(table)
        self.create_table(table)

        rows = self.insert_into_table(table)

        for row in rows:
            self.assertTrue(row.get('lastrowid', False))
