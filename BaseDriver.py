#! $(env python)

from jinja2 import Template

class BaseDriver():
	def jinja(self, param):
		t = Template(param)
		return t.render(uri=self.uri, url=self.url)

	def jinja_params(self, query):
		src = query.get('params', None)

		params = []
		if src != None:
			for param in src:
				params.append( self.jinja(param) )

		return params
