#! /usr/bin/env python3

class TypeImporter():
    def __init__(self, value, component):
        self.type = 'boolean'
        self.errors = []

        self.value = value
        for key in ('as_false', 'reject'):
            setattr(self, key, component.get(key, []))

        self.value = self.value_as_false()

    def validate_reject(self):
        for reject in self.reject:
            local = {
                'this': self.value
            }

            if eval(reject, {}, local):
                err = "'{}' ({}) rejected by '{}'".format(self.value, self.type, reject)
                self.errors.append(err)

        return not bool(self.errors)


    def valid(self):
        return self.validate_reject()


    def value_as_false(self):
        for value in self.as_false:
            if self.value == value: return False

        return self.value


