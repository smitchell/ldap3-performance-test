#!/usr/bin/env python3
import logging
from json.decoder import JSONDecodeError
from urllib.parse import unquote

from flask import Blueprint, Response, make_response
from flask import json
from flask import request
from marshmallow import ValidationError
from requests import models

from api.controllers.ldap_controller import LdapController
from api.dtos.add_entry_request import AddEntryRequest
from api.dtos.modify_entry_request import ModifyEntryRequest
from api.schemas.add_entry_request_schema import AddEntryRequestSchema
from api.schemas.modify_entry_request_schema import ModifyEntryRequestSchema
from api.schemas.search_schema import SearchSchema

gateway_api_blueprint = Blueprint('gateway_api', __name__)
ldap_controller = LdapController()
search_schema = SearchSchema()
modify_entry_request_schema = ModifyEntryRequestSchema()
success = 'success'


def get_blueprint():
    """Return the blueprint for the main app module"""
    return gateway_api_blueprint


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
        return make_response(500)
    content_type = request_resp.headers.get('Content-Type', None)
    if content_type == 'application/json':
        flask_resp: Response = make_response(request_resp.json(), request_resp.status_code)
    else:
        flask_resp: Response = make_response(request_resp.text, request_resp.status_code)
    flask_resp.content_type = content_type
    return flask_resp
