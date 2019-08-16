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

    def modify(self, imported, query):
        op = query['op']
        data = self.render_writes(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(op, params)
            datum['rowcount'] = self.cursor.rowcount

        self.db.commit()

        return data

    def delete(self, imported, query):
        return self.modify(imported, query)

    def get(self, imported, query):
        op = query['op']
        params = self.render_params(imported, query)
        #print(params)
        print(op)
        for param in params:
            print(param, type(param))

        self.cursor.execute(op, params)

        return self.cursor.fetchall()

    def patch(self, imported, query):
        return self.modify(imported, query)

    def post(self, imported, query):
        op = query['op']
        data = self.render_writes(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(op, params)
            datum['lastrowid'] = self.cursor.lastrowid
        self.db.commit()

        return data

    def render_params(self, imported, query):
        params = []
        for param in query.get('params', []):
            params.append(self.inject_imported(imported, param))

        return params

    def inject_imported(self, imported, param):
        source = None
        tag = None
        try:
            source, tag = param.split('.', 1)

        except ValueError:
            pass

        if source in ('args', 'data', 'cookies', 'form', 'headers', 'vars'):
            return imported[source][tag]

        return param

    def render_writes(self, imported, query):
        data = imported['data']
        local = imported.copy()

        if not data:
            data.append({})

        for datum in data:
            datum['params'] = []
            local['data'] = datum

            datum['params'] = self.render_params(local, query)

        return data
