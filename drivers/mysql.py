#! /usr/bin/env python3

import MySQLdb

class Driver:
    def __init__(self, src):
        self.db = MySQLdb.connect(**src)
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.db.close()


    def delete(self, query):
        try:
            self.cursor.execute(query['op'], query['params'])
            self.db.commit()
        except:
            return None

        return self.cursor.rowcount


    def get(self, query):
            try:
                self.cursor.execute(query['op'], query['params'])
            except Exception as e:
                return None

            return self.cursor.fetchall()


    def post(self, imported, query):
        return self.write(query)


    def patch(self, query):
        return self.write(query)


    def write(self, query):
        op = query['op']
        for params in query['params']:
            self.cursor.execute(op, params)
        
        self.db.commit()

        return self.cursor.lastrowid

