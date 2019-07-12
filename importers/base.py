#! /usr/bin/env python3
"""This module contains the base TypeImporter"""


class TypeImporter():
    """The base TypeImporter is the TypeImporter all others should inherit from"""
    def __init__(self, key, rule, value, component):
        self.errors = []
        self.key = key
        self.original = self.value = value
        self.rule = rule

        self.init_type_importer(component)

    def init_type_importer(self, component):
        raise NotImplementedError

    def has_errors(self):
        return bool(self.errors)

    def valid(self):
        raise NotImplementedError

    def load_component(self, component, default, *args):
        for key in args:
            setattr(self, key, component.get(key, default))

    def append_error(self, prompt, *args):
        msg = prompt.format(*args)
        err = "{}['{}'] ({}): {}".format(
            self.key,
            self.rule,
            self.type,
            msg,
        )

        self.errors.append(err)

    def validate_reject(self):
        for reject in self.reject:
            local = {'this': self.value}

            if eval(reject, {}, local):
                self.append_error("was '{}', now '{}', rejected by '{}'",
                                  self.original, self.value, reject)

                return False

        return True
