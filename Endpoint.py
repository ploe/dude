#! /usr/bin/env python3

import re
import yaml

from importlib import import_module

class Endpoint():
    def __init__(self, path):
        with open(path, 'r') as fh:
            self.data = yaml.load( fh.read(), Loader=yaml.Loader )

    def new_importer(self, component):
        tag = "importers.{}".format(component['type'])

        module = import_module(tag)
        new = getattr(module, "Importer")

        return new(component)

    def importer(self, value, component):
        importer = self.new_importer(component)

        return importer.import(value)

    def validate_component(self, component):
        importer = self.new_importer(component)

        return importer.validate()

    def get_pipeline(self, method):
        return self.data[method]

    def run_pipeline(self, client, method):
        pipeline = self.get_pipeline(method)

        for op in pipeline:
            print(op['op'])

    def run_pipeline_until(self, client, method, breakpoint):
        pipeline = self.get_pipeline(method)

        for op in pipeline:
            if op['breakpoint'] == breakpoint:
                break

            print(op['op'])

