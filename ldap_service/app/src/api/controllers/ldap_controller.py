#!/usr/bin/env python3
import json
from typing import Any

from flask import Response, current_app
from ldap3 import Connection, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, DEREF_NEVER, DEREF_SEARCH, DEREF_BASE, \
    DEREF_ALWAYS, BASE, LEVEL, SUBTREE, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_INCREMENT, SAFE_SYNC
from ldap3.core.exceptions import LDAPInvalidDnError
from ldap3.utils.conv import escape_filter_chars

from api.app import app
from api.controllers.connection_manager import ConnectionManager
from api.dtos.add_entry_request import AddEntryRequest
from api.dtos.modify_entry_request import ModifyEntryRequest
from api.dtos.search import Search
from api.dtos.search_results import SearchResults

dereference_aliases_types = dict(
    DEREF_NEVER=DEREF_NEVER,
    DEREF_SEARCH=DEREF_SEARCH,
    DEREF_BASE=DEREF_BASE,
    DEREF_ALWAYS=DEREF_ALWAYS
)

operation_types = dict(
    MODIFY_ADD=MODIFY_ADD,
    MODIFY_DELETE=MODIFY_DELETE,
    MODIFY_REPLACE=MODIFY_REPLACE,
    MODIFY_INCREMENT=MODIFY_INCREMENT
)

search_scope_types = dict(BASE=BASE, LEVEL=LEVEL, SUBTREE=SUBTREE)
mocked_server_name = 'mocked'
success = 'success'
entry_already_exists = 'entryAlreadyExists'

class LdapController:

    def __init__(self):
        with app.app_context():
            self.logger = current_app.logger
        self.connection_manager = ConnectionManager()

    # This method adds a new entry to LDAP. The dn must be unique and must match the dn
    # attribute in the AddEntryRequest.
    def add(self, server_name: str, add_entry_request: AddEntryRequest) -> str:
        connection: Connection = self.connection_manager.get_connection(server_name, None)

        if add_entry_request.controls is None:
            if add_entry_request.attributes is not None:
                response = connection.add(add_entry_request.dn, add_entry_request.object_class,
                               LdapController.scrub_dict(add_entry_request.attributes, True),
                               add_entry_request.controls)
            else:
                response = connection.add(add_entry_request.dn, add_entry_request.object_class, None, add_entry_request.controls)
        elif add_entry_request.attributes is not None:
            response = connection.add(add_entry_request.dn, add_entry_request.object_class,
                           LdapController.scrub_dict(add_entry_request.attributes, True))
        else:
            response = connection.add(add_entry_request.dn, add_entry_request.object_class)

        if isinstance(response, tuple):
            result = response[1]
        else:
            result = connection.result

        result_description = result["description"]
        result_message = result["message"]

        connection.unbind()
        msg = f'{add_entry_request.dn}: {result_description} {result_message}'
        self.logger.info(msg)
        if result_description == success:
            return result_description
        elif result_description == entry_already_exists:
            self.logger.warning(msg)
            return msg
        self.logger.error(msg)
        return msg

    # This method modifies an existing entry ing LDAP. The dn must match an existing entity.
    def modify(self, server_name: str, modify_entry_request: ModifyEntryRequest) -> str:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        changes = modify_entry_request.changes
        for attribute_key in changes:
            attribute = changes[attribute_key]
            temp_dict = {}
            result = []
            for operation in attribute:
                for operation_key in operation.keys():
                    new_key = operation_types[operation_key]
                    if new_key in temp_dict:
                        temp_dict[new_key] += operation[operation_key]
                    else:
                        temp_dict[new_key] = operation[operation_key]

            for key in temp_dict:
                result.append(tuple([key] + temp_dict[key]))
            changes[attribute_key] = result

        if modify_entry_request.controls is not None:
            response = connection.modify(modify_entry_request.dn, changes, modify_entry_request.controls)
        else:
            response = connection.modify(modify_entry_request.dn, changes)
        if isinstance(response, tuple):
            result = response[1]
        else:
            result = connection.result

        result_description = result["description"]
        result_message = result["message"]
        print(result)
        print(type(result))

        connection.unbind()
        msg = f'{modify_entry_request.dn}: {result_description} {result_message}'
        self.logger.info(msg)
        if result_description == success:
            return result_description
        elif result_description == entry_already_exists:
            self.logger.warning(msg)
        else:
            self.logger.error(msg)
        return msg


    def search(self, server_name: str, s: Search) -> SearchResults:
        results = []
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        response = connection.search(search_base=s.search_base,
                          search_filter=s.search_filter,
                          search_scope=search_scope_types[s.search_scope],
                          dereference_aliases=dereference_aliases_types[s.dereference_aliases],
                          attributes=LdapController._convert_attributes_keyword(s.attributes),
                          size_limit=s.size_limit,
                          time_limit=s.time_limit,
                          types_only=s.types_only,
                          get_operational_attributes=s.get_operational_attributes,
                          controls=s.controls,
                          paged_size=s.paged_size,
                          paged_criticality=s.paged_criticality,
                          paged_cookie=s.paged_cookie)

        if isinstance(response, tuple) and response[1] is not None and 'description' in response[1] and response[1]['description'] == success:
            results = self._convert_safe_sync_results(response[2])
        elif connection.result is not None and 'description' in connection.result and connection.result['description'] == success:
            results = self._convert_results(connection.entries)

        connection.unbind()
        return SearchResults(data=results, criteria=s.search_filter)


    def delete(self, server_name: str, dn: Any, controls: Any = None) -> bool:
        connection: Connection = self.connection_manager.get_connection(server_name, None)

        try:
            connection.delete(dn, controls=controls)
            return True
        except LDAPInvalidDnError:
            # Ignore error if the dn does not exist.
            self.logger.warning(f'{dn} could not be found to delete.')
            return True
        finally:
            connection.unbind()

    @staticmethod
    def _convert_results(entries) -> list:
        results = []
        if entries is not None:
            for entry in entries:
                results.append({'dn': entry.entry_dn, 'attributes': entry.entry_attributes_as_dict})
        return results

    @staticmethod
    def _convert_safe_sync_results(entries) -> list:
        results = []
        if entries is not None:
            for entry in entries:
                results.append({'dn': entry['dn'], 'attributes': dict(entry['attributes'])})
        return results

    @staticmethod
    def _convert_attributes_keyword(value) -> Any:
        if value == 'ALL_ATTRIBUTES':
            return ALL_ATTRIBUTES
        if value == 'ALL_OPERATION_ATTRIBUTES':
            return ALL_OPERATIONAL_ATTRIBUTES
        return value

    @staticmethod
    def scrub_json(source) -> None:
        if 'controls' in source:
            controls = source['controls']
            if controls is None or controls == 'None' or len(controls) == 0:
                del source['controls']
        if 'attributes' in source:
            attributes = source['attributes']
            if attributes is None or attributes == 'None' or len(attributes) == 0:
                del source['attributes']
            else:
                # The dn of add_entry_request and modify entry request
                # don't pass validation so only process the attributes.
                attributes = source['attributes']
                for key in attributes:
                    attributes[key] = escape_filter_chars(attributes[key])

    @staticmethod
    def scrub_dict(source, remove_empty: bool = False):
        target = {}
        for key in source:
            value = escape_filter_chars(source[key])
            if remove_empty and (value is None or value == 'None' or len(value) == 0):
                continue
            target[key] = value
        return target
