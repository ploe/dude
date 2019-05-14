import re
import yaml

import Mandators

from MySQLDriver import MySQLDriver as MySQL

class Endpoint():
    def __init__(self, path):
        with open(path, 'r') as fh:
            self.data = yaml.load( fh.read(), Loader=yaml.Loader )

    def mandate(self, value, component):
        tag = "{}Mandator".format(component['type'])

        new = getattr(Mandators, tag)
        mandator = new(component)

        return mandator.mandate(value)

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

