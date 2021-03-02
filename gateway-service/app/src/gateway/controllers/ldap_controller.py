#!/usr/bin/env python3
from typing import Any
from urllib import parse

from flask import Response
from flask import current_app
from requests import get, post, put, delete, RequestException

from gateway.app import app
from gateway.dtos.add_entry_request import AddEntryRequest
from gateway.dtos.modify_entry_request import ModifyEntryRequest
from gateway.dtos.search import Search
from gateway.schemas.add_entry_request_schema import AddEntryRequestSchema
from gateway.schemas.modify_entry_request_schema import ModifyEntryRequestSchema
from gateway.schemas.search_schema import SearchSchema


class LdapController:
    host_url: str

    def __init__(self):
        with app.app_context():
            self.logger = current_app.logger
            self.host_url = app.config['ldap_service_url']
            print(self.host_url)

    def get_health_check(self) -> Response:
        try:
            return get(f'{self.host_url}/api/health_check')
        except RequestException as e:
            self.logger.error(f'{__name__} {e}')
            return self.create_error_response(500, str(e))

    def add(self, add_entry_request: AddEntryRequest, args: dict) -> Response:
        try:
            schema: AddEntryRequestSchema = AddEntryRequestSchema()
            url = LdapController.make_url(f'{self.host_url}/api/entries', args)
            return post(url, json=schema.dumps(add_entry_request))
        except RequestException as e:
            self.logger.error(f'{__name__} {e}', exc_info=True)
            return self.create_error_response(500, str(e))

    def modify(self, modify_entry_request: ModifyEntryRequest, args: dict) -> Response:
        try:
            schema = ModifyEntryRequestSchema()
            modify_json = schema.dumps(modify_entry_request)
            encoded_dn = parse.quote(modify_entry_request.dn)
            url = LdapController.make_url(f'{self.host_url}/api/entry/{encoded_dn}', args)
            return put(
                url,
                json=modify_json)
        except RequestException as e:
            self.logger.error(f'{__name__} {e}', exc_info=True)
            return self.create_error_response(500, str(e))

    def search(self, s: Search, args: dict) -> Response:
        try:
            schema: SearchSchema = SearchSchema()
            url = LdapController.make_url(f'{self.host_url}/api/search', args)
            return post(url, json=schema.dumps(s))
        except RequestException as e:
            self.logger.error(f'{__name__} {e}', exc_info=True)
            return self.create_error_response(500, str(e))

    def delete(self, dn: Any, args: dict) -> Response:
        try:
            encoded_dn = parse.quote(dn)
            url = LdapController.make_url(f'{self.host_url}/api/entry/{encoded_dn}', args)
            return delete(url)
        except RequestException as e:
            self.logger.error(f'{__name__} {e}', exc_info=True)
            return self.create_error_response(500, str(e))

    @staticmethod
    def create_error_response(status_code: int, reason: str = None) -> Response:
        response = Response()
        response.status_code = status_code
        response.reason = reason
        return response

    @staticmethod
    def add_concat(url: str) -> str:
        if url is not None:
            if '?' in url:
                url += '&'
            else:
                url += '?'
        return url

    @staticmethod
    def make_url(url, args: dict):
        if url is not None and args is not None:
            for key in args:
                value = args.get(key, None)
                if value is not None:
                    url = LdapController.add_concat(url)
                    url += f'{key}={value}'
        return url
