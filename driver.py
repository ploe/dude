#! /usr/bin/env python3

import importlib


class Driver():
    def __init__(self, component, method, bank):
        self.bank = bank
        self.component = component
        self.driver = self.get_driver()
        self.method = getattr(self.driver, method.lower())

    def call_method(self, imported):
        return self.method(imported, self.component['query'])

    def get_driver(self):
        driver = self.bank['Driver']

        name = "drivers.{}".format(driver)
        module = importlib.import_module(name)

        new = getattr(module, 'Driver')
        return new(self.bank['Creds'])
