#! /usr/bin/env python3

import importlib
import os

import yaml

from importer import Importer

DOMAIN_PATH = os.getenv('DUDE_DOMAIN_PATH', '.')

class EndpointInvalid(Exception):
    """Raised when the Endpoint is invalid, should 404"""
    pass

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
