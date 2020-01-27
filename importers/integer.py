#! /usr/bin/env python3
"""Integer TypeImporter module"""

from importers.base import TypeImporter as base


class TypeImporter(base):
    """Integer TypeImporter class"""
    def init_type_importer(self, component):
        self.type = 'integer'
        self.load_component(component, [], 'reject')

        self.value_to_integer()

    def value_to_integer(self):
        """Coerces the value to an int, when possible, otherwise it pushes an
        error to the TypeImporter"""
        try:
            self.value = int(self.value)
        except ValueError:
            self.append_error("'{}' invalid integer", self.value)

        except TypeError:
            self.append_error("'{}' invalid type, should be integer",
                              self.value)

        return self.has_errors()

    def valid(self):
        if not self.has_errors():
            self.validate_reject()
        return not self.has_errors()
