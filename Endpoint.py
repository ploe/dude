import yaml

from MySQLDriver import MySQLDriver as MySQL

class Endpoint():
    def __init__(self, path):
        with open("endpoints/test_Endpoint.yml", 'r') as fh:
            self.data = yaml.load( fh.read() )

    def get_pipeline(self, method):
        return self.data[method]

    def run_pipeline(self, client, method):
        pipeline = self.get_pipeline(method)

        for op in pipeline:
            print(op['op'])

    def run_pipeline_until(self, client, method, pause):
        pipeline = self.get_pipeline(method)

        for op in pipeline:
            if op['_pause'] == pause:
                break

            print(op['op'])

