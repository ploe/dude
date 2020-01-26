#! /usr/bin/env python3
"""Transformer module"""

class Transformer():
    """Transformer is the class that drives the Transformers"""
    def __init__(self, transforms):
        for source in ('data', 'group', 'order', 'paginate'):
            component = transforms.get(source, {})
            print(component)

            valid = False
            for valid_type in (dict, list):
                valid = isinstance(component, valid_type)

                if valid:
                    setattr(self, source, component)
                    break

            if not valid:
                raise TypeError
