#! /usr/bin/env python3
"""This module contains the base TypeImporter."""


class TypeImporter():
    """The base TypeImporter is the TypeImporter all child classes should inherit from."""
    def __init__(self, key, rule, value, component):
        self.errors = []
        self.key = key
        self.original = self.value = value
        self.rule = rule

        self.init_type_importer(component)

    def init_type_importer(self, component):
        """Needs defining in each child TypeImporter.
        Runs the child class specific init functions"""
        raise NotImplementedError

    def has_errors(self):
        """Returns True if the TypeImporter generated any errors"""
        return bool(self.errors)

    def valid(self):
        """Needs defining in each child class. Should return True if the data is valid"""
        raise NotImplementedError

    def load_component(self, component, default, *args):
        """Used to unpack the component in to the TypeImporter class"""
        for key in args:
            setattr(self, key, component.get(key, default))

    def append_error(self, prompt, *args):
        """Add a new error message to errors"""
        msg = prompt.format(*args)
        err = "{}['{}'] ({}): {}".format(
            self.key,
            self.rule,
            self.type,
            msg,
        )

        self.errors.append(err)

    def validate_reject(self):
        """Run the eval on the value imported.
		This is development only, and should be considered deprecated"""
        for reject in self.reject:
            local = {'this': self.value}

            if eval(reject, {}, local):
                self.append_error("was '{}', now '{}', rejected by '{}'",
                                  self.original, self.value, reject)

                return False

        return True
