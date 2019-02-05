import unittest

from datetime import datetime

from MySQLDriver import MySQLDriver

class MySQLDriverTestCase(unittest.TestCase):
    def setUp(self):
        src = {
            'host': "127.0.0.1",
            'user': "root",
            'passwd': "+zQx57?4$9",
        }
        
        self.mysql = MySQLDriver(src)
        self.mysql.cursor.execute("""
                CREATE DATABASE pont;
                CREATE TABLE pont.driver_test (
                    name VARCHAR(255),
                    age INT,
                    created DATETIME
                );
        """)


    def tearDown(self):
        self.mysql.cursor.execute("DROP DATABASE pont")

    def created(self):
        return datetime.strptime('2018-10-02 9:13:37', '%Y-%m-%d %H:%M:%S')


    def get(self):
        query = {
            'op': "SELECT * FROM pont.driver_test",
            'params': []
        }

        return self.mysql.get(query)


    def post(self):
        query = {
            'op': "INSERT INTO pont.driver_test (name, age, created) VALUES (%s, %s, %s)",
            'params': ["Myke", 31, self.created()],
        }

        return self.mysql.post(query)


    def test_post(self):
        self.assertNotEqual(self.post(), None)


    def test_get(self):
        self.post()
        rows = self.get()

        self.assertNotEqual(rows, None)

        for row in rows:
            self.assertEqual(row['name'], "Myke")
            self.assertEqual(row['age'], 31)
            self.assertEqual(row['created'], self.created())

