#! /usr/bin/env python3
"""String TypeImporter module"""

from importers.base import TypeImporter as base


class TypeImporter(base):
    """String TypeImporter class"""
    def init_type_importer(self, component):
        self.type = 'string'
        self.load_component(component, [], 'reject')

        self.value_to_string()

    def value_to_string(self):
        """Coerces the value to an string, when possible, otherwise it pushes an
        error to the TypeImporter"""
        try:
            self.value = str(self.value)
        except ValueError:
            self.append_error("'{}' invalid string", self.value)

        except TypeError:
            self.append_error("'{}' invalid type, should be string",
                              self.value)

        return self.has_errors()

    def valid(self):
        if not self.has_errors():
            self.validate_reject()

        return not self.has_errors()
