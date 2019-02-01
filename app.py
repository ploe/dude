import yaml

from flask import abort, Flask, g, jsonify, request
app = Flask(__name__)
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

class MySQLDriver:
    def __init__(self, params):
        self.db = MySQLdb.connect(
  	    host="localhost",
 	    user="root",
  	    passwd="+zQx57?4$9",
  	    db="crud"
	)

	self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
	self.uri = params['uri']
	self.url = params['url']

    def post(member, query):
        params = self.jinja_params(query)

        try:
            self.cursor.execute(query['op'], params)
            self.db.commit()
        except:
            return False

        return self.cursor.lastrowid

class Endpoint:
    def __init__(self, params):
        self.params = struct
        self.db = MySQLDriver()

    def post(uri, url, members=[]):
        method = None

        if uri.member then:
            method = self.struct["POST"]["member"]
        else:
            method = self.struct["POST"]["collection"]

        self.transform(members, method)

        query = method["query"]
        results = []
        for member in self.members():
            results.append(db.post(member, query))

    def transform(members):
        self.members = members

@app.route('/')
def hello_world():
    endpoint = None
    with open('sample.yaml') as data:
        endpoint = yaml.load(data)

    return endpoint.get("name", "")
