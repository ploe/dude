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
            'args': {
                'firstname': 'Jack'
            },
            'cookies': {},
            'form': {
                'firstname': 'David',
                'lucky_number': 6
            },
            'header': {},
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

        return self.driver.post(imported, query)

    def select_query(self, imported, table):
        query = {
            'op':
            "SELECT * FROM {} WHERE firstname=%s and lucky_number=%s ORDER BY id ASC"
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
        rows = self.select_query(imported, table)
        self.drop_table(table)

        data = []
        for datum in imported['data']:
            if (datum['firstname'] == 'David') and (
                    datum['lucky_number'] == 6):

                datum['id'] = datum.pop('lastrowid')
                data.append(datum)

        data = sorted(data, key=lambda datum: datum['id'], reverse=True)

        for row in rows:
            datum = data.pop()

            for key in row:
                self.assertEqual(row[key], datum[key])


#    def test_delete(self):
#        table = 'dude_tests.test_delete_data'
#        self.create_table(table)
#
#        imported = self.get_imported_data()
#
#        self.insert_query(imported, table)
#
#        query = {
#            'op':
#            "DELETE FROM {} WHERE firstname=%s;"
#            .format(table),
#            'params': [
#                '{{ args.firstname }}'
#            ]
#
#        }
#        self.driver.delete(imported, query)
#
#        query = { 'op': "SELECT * FROM {} ORDER BY id ASC".format(table), 'params': []}
#        rows = self.driver.get(imported, query)
#        print(rows)
#        self.drop_table(table)
#
#        data = []
#        for datum in imported['data']:
#            if (datum['firstname'] != 'Jack'):
#                datum['id'] = datum.pop('lastrowid')
#                data.append(datum)
#
#        data = sorted(data, key=lambda datum: datum['id'])
#
#        for row in rows:
#            datum = data.pop()
#
#            for key in row:
#                print(row['firstname'], datum['firstname'])
#
#                print(key, row[key], datum[key])
#                self.assertEqual(row[key], datum[key])

    def test_post(self):
        table = 'dude_tests.test_post_data'
        self.create_table(table)

        imported = self.get_imported_data()

        rows = self.insert_query(imported, table)
        self.drop_table(table)

        for row in rows:
            self.assertTrue(row.get('lastrowid', False))
