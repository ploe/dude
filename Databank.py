import yaml

from MySQLDriver import MySQLDriver as MySQL

class Databank:
    def __init__(self, path):
        with open(path, "r") as fh:
            self.data = yaml.load( fh.read(), Loader=yaml.Loader )

    def connect(self):
        return globals()[ self.data['driver'] ]( self.data['login'] )

