#! /usr/bin/env python3

import re

from jinja2 import Template

class Mandator():
    def __init__(self, component):
        self.component = component

class strMandator(Mandator):
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
        contains = self.component.get('contains', [])

        for substr in contains:
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

