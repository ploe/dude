import unittest

from datetime import datetime

from MySQLDriver import MySQLDriver

class MySQLDriverTestCase(unittest.TestCase):
    def setUp(self):
        src = {
            'host': "127.0.0.1",
            'user': "pont",
            'passwd': "+zQx57?4$9",
        }
        
        self.mysql = MySQLDriver(src)
        self.mysql.cursor.execute("""
                CREATE DATABASE pont;
                CREATE TABLE pont.test_MySQLDriver (
                    id int NOT NULL AUTO_INCREMENT,
                    name VARCHAR(255),
                    age INT,
                    dob DATETIME,
                    PRIMARY KEY (id)
                );
        """)


    def tearDown(self):
        self.mysql.cursor.execute("DROP DATABASE pont")


    def dob(self):
        return datetime.strptime('2018-10-02 9:13:37', '%Y-%m-%d %H:%M:%S')


    def create(self):
        query = {
            'op': "INSERT INTO pont.test_MySQLDriver (name, age, dob) VALUES (%s, %s, %s)",
            'params': ["Myke", 31, self.dob()],
        }

        return self.mysql.create(query)


    def read(self):
        query = {
            'op': "SELECT * FROM pont.test_MySQLDriver",
            'params': []
        }

        return self.mysql.read(query)


    def update(self, rowid):
        query = {
            'op': "UPDATE pont.test_MySQLDriver SET name=%s, age=%s WHERE id=%s",
            'params': ['George', 34, rowid],
        }

        return self.mysql.update(query)


    def delete(self, rowid):
        query = {
            'op': "DELETE FROM pont.test_MySQLDriver WHERE id=%s",
            'params': [rowid],
        }

        return self.mysql.delete(query)


    def test_create(self):
        self.assertNotEqual(self.create(), None)


    def test_read(self):
        self.create()
        rows = self.read()

        self.assertNotEqual(rows, None)

        for row in rows:
            self.assertEqual(row['name'], "Myke")
            self.assertEqual(row['age'], 31)
            self.assertEqual(row['dob'], self.dob())


    def test_update(self):
        rowid = self.create()
        self.update(rowid)

        rows = self.read()
        for row in rows:
            self.assertEqual(row['id'], rowid)
            self.assertEqual(row['name'], "George")
            self.assertEqual(row['age'], 34)
            self.assertEqual(row['dob'], self.dob())


    def test_delete(self):
        rowid = self.create()

        self.assertTrue(self.delete(rowid))


