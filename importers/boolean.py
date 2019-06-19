#! /usr/bin/env python3

class TypeImporter():
    def __init__(self, value, component):
        self.value = value
        for key in ('as_false', 'reject'):
            setattr(self, key, component.get(key, []))

        self.value = self.value_as_false()
        print(value, self.value)

    def validate_reject(self):
        for reject in self.reject:
            local = {
                'this': self.value
            }

            if eval(reject, {}, local):
                return False

        return True

    def valid(self):
        return self.validate_reject()

    def value_as_false(self):
        for value in self.as_false:
            if self.value == value: return False

        return self.value


