#! /usr/bin/env python3

import MySQLdb

from jinja2 import Template


class Driver:
    def __init__(self, bank):
        self.db = MySQLdb.connect(**bank)
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
        return self.write(imported, query)

    def patch(self, query):
        return self.write(query)

    def write(self, imported, query):
        op = query['op']
        data = self.render_query(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(op, params)
            datum['lastrowid'] = self.cursor.lastrowid

        self.db.commit()

        return data

    def render_query(self, imported, query):
        data = imported['data']
        local = imported.copy()

        for datum in data:
            datum['params'] = []
            local['data'] = datum

            for param in query['params']:
                t = Template(param)
                datum['params'].append(t.render(**local))

        return data
