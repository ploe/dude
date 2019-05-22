#! /usr/bin/env python3

import re
import yaml

from importlib import import_module

class Endpoint():
    def __init__(self, path):
        with open(path, 'r') as fh:
            self.data = yaml.load( fh.read(), Loader=yaml.Loader )

    def new_mandator(self, component):
        tag = "mandators.{}".format(component['type'])

        module = import_module(tag)
        new = getattr(module, "Mandator")

        return new(component)

    def mandate(self, value, component):
        mandator = self.new_mandator(component)

        return mandator.mandate(value)

    def validate_component(self, component):
        mandator = self.new_mandator(component)

        return mandator.validate()

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

