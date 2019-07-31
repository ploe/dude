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

def __list_dirs(path):
    dirs = []
    for directory in os.listdir(path):
        src = os.path.join(path, directory)

        if os.path.isdir(src):
            dirs.append(src)

    return dirs

def __load_endpoints():
    src = "{}/endpoints".format(DOMAIN_PATH)

    endpoints = {}
    for path in __list_dirs(src):
        tag = os.path.basename(path)
        endpoints[tag] = __load_yaml_methods(path)

    #print(endpoints)

    return endpoints

def __load_yaml_methods(path):
    endpoint = {}
    for method in ('DELETE', 'GET', 'PATCH', 'POST'):
        filename = os.path.join(path, '{}.yml'.format(method))

        data = {}
        try:
            with open(filename, 'r') as f:
                data = yaml.load(f, Loader=yaml.Loader)
        except FileNotFoundError:
            pass

        endpoint[method] = data

    return endpoint

class Domain():
    def __init__(self, endpoint, request):
        self.endpoint = self.get_endpoint(endpoint)

        tag = request.method
        method = self.endpoint[tag]

        if not method.get('Enabled', False):
            raise EndpointInvalid

        for key in ('Imports', 'Driver', 'Transforms'):
            component = method.get(key, {})
            setattr(self, key.lower(), component)

        self.importer = Importer(self.imports)
        self.driver = Driver(self.driver, request.method)


    def get_endpoint(self, endpoint):
        if '/' in endpoint:
            raise EndpointInvalid

        data = ENDPOINTS[endpoint]
        print(data)

        return data

    def get(self):
        return self.importer, self.driver, None

ENDPOINTS=__load_endpoints()
