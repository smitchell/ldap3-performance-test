#!/usr/bin/env python3
import logging
from typing import Any
from urllib.parse import unquote
import socket

from flask import Blueprint, Response, make_response
from flask import json
from flask import request

from ldap.controllers.ldap_controller import LdapController
from ldap.dtos.add_entry_request import AddEntryRequest
from ldap.dtos.health_check import HealthCheck
from ldap.dtos.modify_entry_request import ModifyEntryRequest
from ldap.dtos.search_results import SearchResults
from ldap.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap.schemas.health_check_schema import HealthCheckSchema
from ldap.schemas.modify_entry_request_schema import ModifyEntryRequestSchema
from ldap.schemas.search_results_schema import SearchResultsSchema
from ldap.schemas.search_schema import SearchSchema

ldap_api_blueprint = Blueprint('ldap_api', __name__)
ldap_controller = LdapController()
search_schema = SearchSchema()
modify_entry_request_schema = ModifyEntryRequestSchema()
success = 'success'

def get_blueprint():
    """Return the blueprint for the main app module"""
    return ldap_api_blueprint

@ldap_api_blueprint.route('/api/health_check', methods=['GET'])
def get_gateway_health_check() -> Response:
    health_check = HealthCheck(__name__)
    health_check.hostname = socket.gethostname()
    try:
        health_check.ip_addr = socket.gethostbyname(health_check.hostname)
    except socket.gaierror as e:
        logging.warning(f'socket.gethostbyname failed for {health_check.hostname} {e}')
    return make_response(HealthCheckSchema().dump(health_check), 200)


@ldap_api_blueprint.route('/api/entries', methods=['POST'])
def add_entry() -> Response:
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    print(json_data)
    if type(json_data) == dict:
        add_entry_request: AddEntryRequest = AddEntryRequestSchema().load(json_data)
    else:
        add_entry_request: AddEntryRequest = AddEntryRequestSchema().load(json.loads(json_data))

    result: str = ldap_controller.add(_get_name(request.args), add_entry_request)
    if result == success:
        return make_response('OK', 201)
    elif 'entryAlreadyExists' in result:
        return make_text_response(result, 400)
    return make_text_response(result, 500)


@ldap_api_blueprint.route('/api/entry/<string:encodedDn>', methods=['GET'])
def get_entry(encodedDn: str) -> Response:
    if encodedDn is None:
        return make_text_response('Expected query parameter "dn", but found none', 400)

    data = {
        'search_base': unquote(encodedDn),
        'search_filter': '(objectClass=*)',
        'search_scope': 'BASE',
        'attributes': 'ALL_ATTRIBUTES'
    }

    results: SearchResults = ldap_controller.search(_get_name(request.args), search_schema.load(data))
    return make_response(SearchResultsSchema().dumps(results), 200)


@ldap_api_blueprint.route('/api/entry/<string:dn>', methods=['PUT'])
def modify_entry(dn: str) -> Response:
    if dn is None:
        return make_text_response('Expected query parameter "dn", but found none', 400)
    content_dn = unquote(dn)
    if content_dn != dn:
        return make_text_response(f'Path dn {dn} does not match content dn {content_dn}', 400)

    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    if type(json_data) == dict:
        modify_entry_request: ModifyEntryRequest = modify_entry_request_schema.load(json_data)
    else:
        modify_entry_request: ModifyEntryRequest = modify_entry_request_schema.load(json.loads(json_data))
    result = ldap_controller.modify(_get_name(request.args), modify_entry_request)
    if result == success:
        return make_response('OK', 200)
    elif 'noSuchObject' in result:
        return make_text_response(result, 400)
    return make_text_response(result, 500)


@ldap_api_blueprint.route('/api/search', methods=['POST'])
def search() -> Response:
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    if type(json_data) == dict:
        results: SearchResults = ldap_controller.search(_get_name(request.args), search_schema.load(json_data))
    else:
        results: SearchResults = ldap_controller.search(_get_name(request.args), search_schema.load(json.loads(json_data)))
    return make_response(SearchResultsSchema().dumps(results), 200)


@ldap_api_blueprint.route('/api/entry/<string:dn>', methods=['DELETE'])
def delete_entry(dn: str) -> Response:
    return make_response(json.dumps(ldap_controller.delete(_get_name(request.args), unquote(dn))), 205)


def _get_name(args) -> str:
    if 'server_name' in args:
        server_name = args['server_name']
    else:
        server_name = 'main'

    return server_name


def _get_dn(args) -> Any:
    if 'dn' not in args:
        return None
    dn = args['dn']
    return unquote(dn)


def make_text_response(message: str, code: int):
    flask_resp = make_response(message, code)
    flask_resp.content_type = 'plain/text'
    return flask_resp
