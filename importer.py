#! /usr/bin/env python3
"""Importer module"""

import importlib

from jinja2 import Template


class Importer():
    """Importer class"""

    # pylint: disable=too-many-instance-attributes
    # With the 7 types of input and the list of errors the attributes come to 8.
    # Depending on how I decide to use this I might remove some of these
    # sources.

    def __init__(self, imports):
        self.errors = []
        self.args = {}
        self.cookies = {}
        self.data = {}
        self.form = {}
        self.headers = {}

        self.imported = {}

        for source in ('args', 'cookies', 'data', 'form', 'headers'):
            component = imports.get(source, {})

            # If the component is not a dict we're in trouble, so break now.
            if not isinstance(component, dict):
                raise TypeError

            setattr(self, source, imports.get(source, {}))

        variables = imports.get('vars', [])

        if isinstance(variables, dict):
            variables = [variables]

        if not isinstance(variables, list):
            raise TypeError

        self.vars = variables

    @staticmethod
    def get_type_importer(source, tag, value, component):
        """Fetch the correct TypeImporter class based on the type in the component"""
        name = "importers.{}".format(component['type'])
        module = importlib.import_module(name)

        type_importer = getattr(module, 'TypeImporter')
        return type_importer(source, tag, value, component)

    def import_payload(self, payload, components, source):
        """Imports the payload for the components in source"""
        self.imported[source] = imported = {}
        for tag in components:
            component = components[tag]

            value = payload.get(tag, None)
            if not value:
                err = "{}['{}'] ({}): not found".format(
                    source, tag, component['type'])

                self.errors.append(err)
                continue

            type_importer = self.get_type_importer(source, tag, value,
                                                   component)
            if type_importer.valid():
                imported[tag] = type_importer.value

            self.errors.extend(type_importer.errors)

    def import_data(self, data):
        """Imports the payload in the data"""
        self.imported['data'] = imported = []
        if isinstance(data, dict):
            data = [data]

        if isinstance(data, list):
            for datum in data:
                imported.append(self.import_payload(datum, self.data, 'data'))

    def import_vars(self):
        """Import the vars, rendering them from a jinja2 template"""
        if self.errors:
            return

        self.imported['vars'] = imported = {}
        for iteration in self.vars:
            for tag in iteration:
                component = iteration[tag]

                template = component.pop('template')
                jinja_t = Template(template)
                value = jinja_t.render(**self.imported)

                type_importer = self.get_type_importer('vars', tag, value,
                                                       component)
                if type_importer.valid():
                    imported[tag] = type_importer.value

                self.errors.extend(type_importer.errors)

    def import_request(self, request):
        """Iterates over the features of the request, to populate the Importer"""
        for source in ('args', 'cookies', 'form', 'headers'):
            payload = getattr(request, source)
            components = getattr(self, source)

            self.import_payload(payload, components, source)

        self.import_data(request.json)
        self.import_vars()
        return not bool(self.errors)
