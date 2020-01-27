#! /usr/bin/env python3
"""Float TypeImporter module"""

from importers.base import TypeImporter as base


class TypeImporter(base):
    """Float TypeImporter class"""
    def init_type_importer(self, component):
        self.type = 'float'
        self.load_component(component, [], 'reject')

        self.value_to_float()

    def value_to_float(self):
        """Coerces the value to a float, when possible, otherwise it pushes an
        error to the Importer"""
        try:
            self.value = float(self.value)

        except ValueError:
            self.append_error("'{}' invalid float", self.value)

        except TypeError:
            self.append_error("'{}' invalid type, should be float", self.value)

        return self.has_errors()

    def valid(self):
        if not self.has_errors():
            self.validate_reject()

        return not self.has_errors()
