#! /usr/bin/env python3

import os

import yaml

class EndpointInvalid(Exception):
    """Raised when the Endpoint is invalid, should 404"""
    pass

class Importer():
    def __init__(self, imports, request):
        self.imports = imports

    def load(self):


DOMAIN_PATH = os.getenv('DUDE_DOMAIN_PATH', '.')

class Domain():
    def __init__(self, endpoint, request):
        self.endpoint = self.get_endpoint(endpoint, request)

        tag = self.get_method_tag(request.method)
        component = self.endpoint[tag.upper()]

        self.imports = component.get('Imports', {})
        self.importer = Importer(self.imports, request)

        self.driver = component.get('Driver', {})
        self.transforms = component.get('Transforms', {})


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
        return self.importer, None, None
