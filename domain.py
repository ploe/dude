#! /usr/bin/env python3

import importlib
import os

import yaml

from jinja2 import Template

DOMAIN_PATH = os.getenv('DUDE_DOMAIN_PATH', '.')


class EndpointInvalid(Exception):
    """Raised when the Endpoint is invalid, should 404"""
    pass


class Importer():
    def __init__(self, imports):
        self.errors = []
        # each of the following components components in the Imports
        # should be set as attributes
        for source in ('args', 'cookies', 'data', 'form', 'headers'):
            component = imports.get(source, {})

            # If the component is not a dict we're in trouble, so break now.
            if type(component) is not dict:
                raise TypeError

            setattr(self, source, imports.get(source, {}))

        variables = imports.get('vars', [])

        if type(variables) is dict:
            variables = [variables]

        if type(variables) is not list:
            raise TypeError

        self.vars = variables

    def get_type_importer(self, source, tag, value, component):
        name = "importers.{}".format(component['type'])
        module = importlib.import_module(name)

        type_importer = getattr(module, 'TypeImporter')
        return type_importer(source, tag, value, component)

    def import_payload(self, payload, components, source):
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
        self.imported['data'] = imported = []
        if isinstance(data, dict):
            data = [data]

        if isinstance(data, list):
            for datum in data:
                imported.append(self.import_payload(datum, self.data, 'data'))

    def import_vars(self):
        self.imported['vars'] = imported = {}
        for iteration in self.vars:
            for tag in iteration:
                component = iteration[tag]
                template = component.pop('template')
                t = Template(template)
                value = t.render(**self.imported)

                type_importer = self.get_type_importer('vars', tag, value,
                                                       component)
                if type_importer.valid():
                    imported[tag] = type_importer.value

                self.errors.extend(type_importer.errors)

    def import_request(self, request):
        self.imported = {}
        for source in ('args', 'cookies', 'form', 'headers'):
            payload = getattr(request, source)
            components = getattr(self, source)

            self.import_payload(payload, components, source)

        self.import_data(request.json)
        self.import_vars()

        return not bool(self.errors)


class Driver():
    def __init__(self, component, method):
        self.bank = self.get_bank(component['bank'])
        self.driver = self.get_driver()
        self.method = getattr(self.driver, method.lower())

    def call_method(self):
        return self.method()

    def get_bank(self, bank):
        data = None
        src = "{}/banks/{}.yml".format(DOMAIN_PATH, bank)

        with open(src, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)

        return data

    def get_driver(self):
        driver = self.bank['Driver']

        name = "drivers.{}".format(driver)
        module = importlib.import_module(name)

        new = getattr(module, 'Driver')
        return new(self.bank['Creds'])


class Domain():
    def __init__(self, endpoint, request):
        self.endpoint = self.get_endpoint(endpoint, request)

        tag = self.get_method_tag(request.method)
        method = self.endpoint[tag.upper()]

        for key in ('Imports', 'Driver', 'Transforms'):
            component = method.get(key, {})
            setattr(self, key.lower(), component)

        self.importer = Importer(self.imports)
        self.driver = Driver(self.driver, request.method)

    def get_endpoint(self, endpoint, request):
        if '/' in endpoint:
            raise EndpointInvalid

        data = None
        src = "{}/endpoints/{}.yml".format(DOMAIN_PATH, endpoint)

        with open(src, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)

        if data['Enabled'] == False:
            raise EndpointInvalid

        return data

    def get_method_tag(self, method):
        return {
            'POST': 'create',
            'GET': 'read',
            'PATCH': 'update',
            'DELETE': 'delete'
        }[method]

    def get(self):
        return self.importer, self.driver, None
