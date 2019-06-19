#! /usr/bin/env python3

class TypeImporter():
    def __init__(self, key, rule, value, component):
        self.errors = []
        self.key = key
        self.original = self.value = value
        self.rule = rule
        self.type = 'boolean'

        for key in ('as_false', 'reject'):
            setattr(self, key, component.get(key, []))

        self.value = self.value_as_false()

    def validate_reject(self):
        for reject in self.reject:
            local = {
                'this': self.value
            }

            if eval(reject, {}, local):
                err = "{}['{}'] ({}): was '{}', now '{}', rejected by '{}'".format(
                        self.key,
                        self.rule, 
                        self.type, 
                        self.original, 
                        self.value, 
                        reject)

                self.errors.append(err)

        return not bool(self.errors)


    def valid(self):
        return self.validate_reject()


    def value_as_false(self):
        for value in self.as_false:
            if self.value == value: return False

        return self.value


