#! /usr/bin/env python3
"""Boolean TypeImporter module"""

from importers.base import TypeImporter as base


class TypeImporter(base):
    """Boolean TypeImporter class"""
    def __init__(self, source, rule, value, component):
        super().__init__(source, rule, value, component)
        self.as_false = []

    def init_type_importer(self, component):
        self.type = 'boolean'
        self.load_component(component, [], 'reject', 'as_false')

        self.value = self.value_as_false()

    def valid(self):
        return self.validate_reject()

    def value_as_false(self):
        """If the value matches one of the values in 'as_false', this returns False
        otherwise it just returns the value unchanged"""
        for value in self.as_false:
            if self.value == value:
                return False

        return self.value
