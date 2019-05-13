import yaml

from MySQLDriver import MySQLDriver as MySQL

class Mandator():
    def __init__(self, component):
        self.component = component
        self.type_tag = self.get_type_tag()
        self.type = getattr(self, self.type_tag)

    def get_type_tag(self):
        return "type_{}".format(component['type'])

    def type_str(self, value):
        return str(value)

class Endpoint():
    def __init__(self, path):
        with open(path, 'r') as fh:
            self.data = yaml.load( fh.read(), Loader=yaml.Loader )

    def mandate(self, value, component):
        mandator = Mandator(component)
        return mandator.type(value)

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

