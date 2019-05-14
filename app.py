#! /usr/bin/env python3

import yaml

from flask import abort, Flask, g, jsonify, request
app = Flask(__name__)
from jinja2 import Template

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
