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

    def delete(self, imported, query):
        op = query['op']
        data = self.render_writes(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(op, params)

        self.db.commit()

    def get(self, imported, query):
        op = query['op']
        params = self.render_params(imported, query)

        self.cursor.execute(op, params)

        return self.cursor.fetchall()

    def post(self, imported, query):
        return self.write(imported, query)

    def patch(self, query):
        return self.write(query)

    def write(self, imported, query):
        op = query['op']
        data = self.render_writes(imported, query)

        for datum in data:
            params = datum.pop('params')
            self.cursor.execute(op, params)
            datum['lastrowid'] = self.cursor.lastrowid
        self.db.commit()

        return data

    def render_params(self, imported, query):
        rendered = []
        for param in query['params']:
            t = Template(param)
            rendered.append(t.render(**imported))

        return rendered

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

            for param in query['params']:
                datum['params'].append(self.inject_imported(local, param))

        return data
