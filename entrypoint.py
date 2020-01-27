#! /usr/bin/env python3
"""The Flask entrypoint to dude"""

from flask import Flask, abort, jsonify, request

from domain import Domain

APP = Flask(__name__)


@APP.route('/', methods=['GET'])
def status():
    """GET-ing '/' will tell you if the service is up"""
    return 'up!'


@APP.route('/favicon.ico', methods=['GET'])
def favicon():
    """Will add a static favicon at some point in the future"""
    abort(404)


@APP.route('/<path:endpoint>', methods=['OPTIONS'])
def endpoint_options(endpoint):
    """Placeholder for CORS stuff"""
    error = "OPTIONS {endpoint} not implemented".format(endpoint=endpoint)
    print(error)
    abort(404)


@APP.route('/<path:endpoint>', methods=['DELETE', 'GET', 'POST', 'PATCH'])
def endpoint_method(endpoint):
    """The endpoint that drives the dude pipeline"""
    print("get endpoint")
    domain = Domain(endpoint, request)
    importer, driver, transformer = domain.get()

    if not importer.import_request(request):
        return jsonify(importer.errors)

    #print(driver.method(importer.imported))
    #
    # transformer.transform(driver.data)

    # return Response(jsonify(transformer.data()))
    return jsonify(driver.call_method(importer.imported))
