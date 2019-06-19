#! /usr/bin/env python3

import os

import yaml

DOMAIN_PATH = os.getenv('DUDE_DOMAIN_PATH', '.')


class EndpointInvalid(Exception):
	"""Raised when the Endpoint is invalid, should 404"""
	pass


class Importer():
	def __init__(self, imports):
		self.errors = []
		# each of the following rules components in the Imports
		# should be set as attributes
		for key in ('args', 'cookies', 'data', 'form', 'headers'):
			component = imports.get(key, {})

			# If the component is not a dict we're in trouble, so break now.
			if type(component) is not dict:
				raise TypeError

			setattr(self, key, imports.get(key, {}))


	def load_from_rules(self, data, rules, key):
		imported = {}
		for rule in rules:
			component = rules[rule]
			value = data.get(rule, None)
			if value:
				imported[rule] = value
				print(rule, value)
			else:
				err = "'{}' ({}) was not in '{}'".format(rule, component['type'], key)
				self.errors.append(err)

		return imported


	def load_data(self, data):
		print(data)
		if isinstance(data, dict):
			data = [data]

		imported = []
		if isinstance(data, list):
			for datum in data:
				print(datum)
				imported.append( self.load_from_rules(datum, self.data, 'data') )

		return imported


	def load(self, request):
		self.imported = {}
		for key in ('args', 'cookies', 'form', 'headers'):
			data = getattr(request, key)
			rules = getattr(self, key)

			self.imported[key] = self.load_from_rules(data, rules, key)

		self.imported['data'] = self.load_data(request.json)

		return bool(self.errors)


class Domain():
	def __init__(self, endpoint, request):
		self.endpoint = self.get_endpoint(endpoint, request)

		tag = self.get_method_tag(request.method)
		method = self.endpoint[tag.upper()]

		for key in ('Imports', 'Driver', 'Transforms'):
			component = method.get(key, {})
			setattr(self, key.lower(), component)

		self.importer = Importer(self.imports)


	def get_endpoint(self, endpoint, request):
		if '/' in endpoint:
			raise EndpointInvalid

		data = None
		src = "{}/endpoints/{}.yml".format(DOMAIN_PATH, endpoint)

		with open(src, 'r') as f:
			data = yaml.load(f, Loader=yaml.Loader)

		if data['Enabled'] == False:
			raise EndpointInvalid

		return data

	def get_method_tag(self, method):
		return {
			'POST': 'create',
			'GET': 'read',
			'PATCH': 'update',
			'DELETE': 'delete'
		}[method]


	def get(self):
		return self.importer, None, None


