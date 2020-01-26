#! /usr/bin/env python3
"""MySQL Driver module"""

import MySQLdb


class Driver:
    """MySQL Driver class"""
    def __init__(self, bank):
        self.database = MySQLdb.connect(**bank)
        self.cursor = self.database.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.database.close()

    def modify(self, imported, query):
        """UPDATE or DELETE query, returns rowcount"""
        operation = query['op']
        data = self.render_writes(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(operation, params)
            datum['rowcount'] = self.cursor.rowcount

        self.database.commit()

        return data

    def delete(self, imported, query):
        """DELETE method/query, returns rowcount"""
        return self.modify(imported, query)

    def get(self, imported, query):
        """GET method, SELECT query, returns SELECT results"""
        operation = query['op']
        params = self.render_params(imported, query)
        for param in params:
            print(param, type(param))

        self.cursor.execute(operation, params)

        return self.cursor.fetchall()

    def patch(self, imported, query):
        """PATCH method, UPDATE query, returns rowcount"""
        return self.modify(imported, query)

    def post(self, imported, query):
        """POST method, UPDATE qurty, returns imported data with lastrowid added"""
        operation = query['op']
        data = self.render_writes(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(operation, params)
            datum['lastrowid'] = self.cursor.lastrowid

        self.database.commit()

        return data

    def render_params(self, imported, query):
        """Returns the params for the query"""
        params = []
        for param in query.get('params', []):
            params.append(self.inject_imported(imported, param))

        return params

    @staticmethod
    def inject_imported(imported, param):
        """Interpolates data from the specified source, or defaults to just using
        it as a string"""

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
        """Builds up the data and params for an INSERT query"""
        data = imported['data']
        local = imported.copy()

        if not data:
            data.append({})

        for datum in data:
            datum['params'] = []
            local['data'] = datum

            datum['params'] = self.render_params(local, query)

        return data
