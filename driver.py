#! /usr/bin/env python3
"""Driver module"""

import importlib


class Driver():
    """Driver class"""
    def __init__(self, component, method, bank):
        self.bank = bank
        self.component = component
        self.driver = self.get_driver()
        self.method = getattr(self.driver, method.lower())

    def call_method(self, imported):
        """Call the method for the selected driver, returns the specific results"""
        return self.method(imported, self.component['query'])

    def get_driver(self):
        """Returns the driver specified in the databank credentials"""
        driver = self.bank['Driver']

        name = "drivers.{}".format(driver)
        module = importlib.import_module(name)

        new = getattr(module, 'Driver')
        return new(self.bank['Creds'])
