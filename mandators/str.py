#! /usr/bin/env python3

import re

from jinja2 import Template

import mandators.base

class Mandator(mandators.base.Mandator):
    def mandate(self, value):
        try:
            value = str(value)
        except:
            return None

        for method in [
                self.contains,
                self.re,
                self.deny,
        ]:
            if not method(value):
                return None

        return value


    def contains(self, value):
        contains = self.component.get('contains', {})
        substrings = contains.get('values', [])

        for substr in substrings:
            if not substr in value: return False

        return True


    def deny(self, value):
        expressions = self.component.get('deny', [])

        for expr in expressions:
            logic = '{{% if {} %}}True{{% else %}}False{{% endif %}}'.format(expr)

            template = Template(logic)
            if template.render(this=value) == "True":
                return False

        return True


    def re(self, value):
        patterns = self.component.get('re', [])

        for pattern in patterns:
            if not re.search(pattern, value, flags=0): return False

        return True


    def validate(self):
        return self.validate_contains()


    def validate_contains(self):
        contains = self.component.get('contains', {})

        if not contains['op'] in ('accept', 'deny'):
            return False

        values =  type(contains['values'])
        if not values in (str, list):
            return False

        if values is str:
            contains['values'] = [contains['values']]

        return True


