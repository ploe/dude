#! /usr/bin/env python3
"""Domain module"""

import os

import yaml

from driver import Driver
from importer import Importer
from transformer import Transformer


class EndpointInvalid(Exception):
    """Raised when the Endpoint is invalid, should 404"""


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

    return endpoints


def __open_yaml(filename):
    data = {}
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=yaml.Loader)
    except FileNotFoundError:
        pass

    return data


def __load_yaml_methods(path):
    endpoint = {}
    for method in ('DELETE', 'GET', 'PATCH', 'POST'):
        filename = os.path.join(path, '{}.yml'.format(method))
        endpoint[method] = __open_yaml(filename)

    return endpoint


def load_yaml_bank(bank):
    """Imports the bank credentials from a YAML file"""
    src = "{}.yml".format(bank)
    filename = os.path.join(DOMAIN_PATH, 'banks', src)

    return __open_yaml(filename)


class Domain():
    """Domain class represents every endpoint that is loaded at start-up"""
    def __init__(self, endpoint, request):
        self.endpoint = self.get_endpoint(endpoint)

        tag = request.method
        method = self.endpoint[tag]

        if not method.get('Enabled', True):
            raise EndpointInvalid

        self.imports = None
        self.driver = None
        self.transforms = None

        for key in ('Imports', 'Driver', 'Transforms'):
            component = method.get(key, {})
            setattr(self, key.lower(), component)

        self.importer = Importer(self.imports)
        self.transformer = Transformer(self.transforms)

        bank = load_yaml_bank(method['Driver']['bank'])
        self.driver = Driver(self.driver, request.method, bank)

    @staticmethod
    def get_endpoint(endpoint):
        """Returns specific endoint from dict of ENDPOINTS"""
        if '/' in endpoint:
            raise EndpointInvalid

        data = ENDPOINTS[endpoint]

        return data

    def get(self):
        """Returns the Importer, Driver and Transformer"""
        return self.importer, self.driver, None


DOMAIN_PATH = os.getenv('DUDE_DOMAIN_PATH', '.')
DOMAIN_DRIVER = os.getenv('DUDE_DOMAIN_DRIVER', 'dir')
ENDPOINTS = __load_endpoints()
