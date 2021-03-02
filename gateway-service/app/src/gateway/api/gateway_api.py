#!/usr/bin/env python3
import logging
from json.decoder import JSONDecodeError
from urllib.parse import unquote

from flask import Blueprint, Response, make_response
from flask import json
from flask import request
from gateway.schemas.health_check_schema import HealthCheckSchema

from gateway.dtos.health_check import HealthCheck
from marshmallow import ValidationError
from requests import models
import socket
from gateway.controllers.ldap_controller import LdapController
from gateway.dtos.add_entry_request import AddEntryRequest
from gateway.dtos.modify_entry_request import ModifyEntryRequest
from gateway.schemas.add_entry_request_schema import AddEntryRequestSchema
from gateway.schemas.modify_entry_request_schema import ModifyEntryRequestSchema
from gateway.schemas.search_schema import SearchSchema

gateway_api_blueprint = Blueprint('gateway_api', __name__)
ldap_controller = LdapController()
search_schema = SearchSchema()
modify_entry_request_schema = ModifyEntryRequestSchema()
success = 'success'


def get_blueprint():
    """Return the blueprint for the main app module"""
    return gateway_api_blueprint

@gateway_api_blueprint.route('/api/health_check', methods=['GET'])
def get_gateway_health_check() -> Response:
    health_check = HealthCheck(__name__)
    health_check.hostname = socket.gethostname()
    try:
        health_check.ip_addr = socket.gethostbyname(health_check.hostname)
    except socket.gaierror as e:
        logging.warning(f'socket.gethostbyname failed for {health_check.hostname} {e}')
    return make_response(HealthCheckSchema().dump(health_check), 200)


@gateway_api_blueprint.route('/api/ldap/health_check', methods=['GET'])
def get_ldap_health_check() -> Response:
    request_resp: models.Response = ldap_controller.get_health_check()
    return _flask_resp(request_resp)


@gateway_api_blueprint.route('/api/entries', methods=['POST'])
def add_entry() -> Response:
    try:
        data = request.get_data(as_text=True)
        json_data = json.loads(data)
        add_entry_request_schema = AddEntryRequestSchema()
        add_entry_request: AddEntryRequest = add_entry_request_schema.load(json_data)
        request_resp: models.Response = ldap_controller.add(add_entry_request, request.args)
        return _flask_resp(request_resp)
    except JSONDecodeError as e:
        message = f'The payload was not valid JSON: {e}'
        logging.error(message, exc_info=True)
        return make_text_response(message, 400)
    except ValidationError as e:
        message = f'Schema validation failed: {e}'
        logging.error(message, exc_info=True)
        return make_text_response(message, 400)
    except Exception as e:
        logging.error(str(e), exc_info=True)
        return make_text_response(str(e), 500)


@gateway_api_blueprint.route('/api/entry/<string:encoded_dn>', methods=['GET'])
def get_entry(encoded_dn: str) -> Response:
    try:
        if encoded_dn is None:
            return make_text_response('Expected query parameter "dn", but found none', 400)

        data = {
            'search_base': unquote(encoded_dn),
            'search_filter': '(objectClass=*)',
            'search_scope': 'BASE',
            'attributes': 'ALL_ATTRIBUTES'
        }

        request_resp: models.Response = ldap_controller.search(search_schema.load(data), request.args)
        return _flask_resp(request_resp)
    except Exception as e:
        logging.error(str(e), exc_info=True)
        return make_text_response(str(e), 500)


@gateway_api_blueprint.route('/api/entry/<string:dn>', methods=['PUT'])
def modify_entry(dn: str) -> Response:
    try:
        if dn is None:
            return make_text_response('Expected query parameter "dn", but found none', 400)
        content_dn = unquote(dn)
        if content_dn != dn:
            return make_text_response(f'Path dn {dn} does not match content dn {content_dn}', 400)

        data = request.get_data(as_text=True)
        json_data = json.loads(data)
        modify_entry_request: ModifyEntryRequest = modify_entry_request_schema.load(json_data)
        request_resp: models.Response = ldap_controller.modify(modify_entry_request, request.args)
        return _flask_resp(request_resp)
    except Exception as e:
        logging.error(str(e), exc_info=True)
        return make_text_response(str(e), 500)


@gateway_api_blueprint.route('/api/search', methods=['POST'])
def search() -> Response:
    try:
        data = request.get_data(as_text=True)
        json_data = json.loads(data)
        request_resp: models.Response = ldap_controller.search(search_schema.load(json_data), request.args)
        return _flask_resp(request_resp)
    except Exception as e:
        logging.error(str(e), exc_info=True)
        return make_text_response(str(e), 500)


@gateway_api_blueprint.route('/api/entry/<string:dn>', methods=['DELETE'])
def delete_entry(dn: str) -> Response:
    try:
        request_resp: models.Response = ldap_controller.delete(unquote(dn), request.args)
        return _flask_resp(request_resp)
    except Exception as e:
        logging.error(str(e), exc_info=True)
        return make_text_response(str(e), 500)


def make_text_response(message: str, code: int):
    flask_resp = make_response(message, code)
    flask_resp.content_type = 'plain/text'
    return flask_resp

def _flask_resp(request_resp: models.Response) -> Response:
    if request_resp is None:
        logging.warning(f'{__name__} _flask_resp is None')
        return make_response(500)
    content_type = request_resp.headers.get('Content-Type', None)
    logging.info(f'{__name__} _flask_resp content_type is {content_type}: {request_resp.content}')
    if content_type == 'application/json':
        flask_resp: Response = make_response(request_resp.json(), request_resp.status_code)
    else:
        flask_resp: Response = make_response(request_resp.content, request_resp.status_code)
    flask_resp.content_type = content_type
    return flask_resp
