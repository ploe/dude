#! /usr/bin/env python3

import importlib
import os

import yaml

DOMAIN_PATH = os.getenv('DUDE_DOMAIN_PATH', '.')


class EndpointInvalid(Exception):
    """Raised when the Endpoint is invalid, should 404"""
    pass


class Importer():
    def __init__(self, imports):
        self.errors = []
        # each of the following rules components in the Imports
        # should be set as attributes
        for key in ('args', 'cookies', 'data', 'form', 'headers', 'vars'):
            component = imports.get(key, {})

            # If the component is not a dict we're in trouble, so break now.
            if type(component) is not dict:
                raise TypeError

            setattr(self, key, imports.get(key, {}))

    def get_type_importer(self, key, rule, value, component):
        name = "importers.{}".format(component['type'])
        module = importlib.import_module(name)

        TypeImporter = getattr(module, 'TypeImporter')
        return TypeImporter(key, rule, value, component)

    def load_from_rules(self, data, rules, key):
        imported = {}
        for rule in rules:
            component = rules[rule]

            value = data.get(rule, None)
            if not value:
                err = "{}['{}'] ({}): not found".format(
                    key, rule, component['type'])

                self.errors.append(err)
                continue

            type_importer = self.get_type_importer(key, rule, value, component)
            if type_importer.valid():
                imported[rule] = type_importer.value

            self.errors.extend(type_importer.errors)

        return imported

    def load_data(self, data):
        if isinstance(data, dict):
            data = [data]

        imported = []
        if isinstance(data, list):
            for datum in data:
                imported.append(self.load_from_rules(datum, self.data, 'data'))

        return imported

    def load_vars(self):
        if isinstance(self.vars, dict):
            self.vars = [self.vars]

        if not isinstance(self.vars, list):
            return
        
        imported = {}
        for iteration in self.vars:
            for var in iteration:
                #imported[var] = 

    def load(self, request):
        self.imported = {}
        for key in ('args', 'cookies', 'form', 'headers'):
            data = getattr(request, key)
            rules = getattr(self, key)

            self.imported[key] = self.load_from_rules(data, rules, key)

        self.imported['data'] = self.load_data(request.json)
        self.imported['vars'] = self.load_vars()

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
