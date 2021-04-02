#!/usr/bin/env python3
import json
from typing import Any, List

from flask import current_app
from ldap3 import Connection, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, DEREF_NEVER, DEREF_SEARCH, DEREF_BASE, \
    DEREF_ALWAYS, BASE, LEVEL, SUBTREE, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_INCREMENT
from ldap3.abstract.entry import EntryBase, Entry
from ldap3.core.exceptions import LDAPInvalidDnError, LDAPNoSuchObjectResult
from ldap3.core.usage import ConnectionUsage
from ldap3.utils.conv import escape_filter_chars

from ldap.app import app
from ldap.controllers.connection_manager import ConnectionManager
from ldap.dtos.add_entry_request import AddEntryRequest
from ldap.dtos.modify_entry_request import ModifyEntryRequest
from ldap.dtos.search import Search
from ldap.dtos.search_results import SearchResults


class LdapController:
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
    insufficient_access_rights = 'insufficientAccessRights'

    def __init__(self):
        with app.app_context():
            self.logger = current_app.logger
        self.connection_manager = ConnectionManager()

    # This method adds a new entry to LDAP. The dn must be unique and must match the dn
    # attribute in the AddEntryRequest.
    def add(self, server_name: str, add_entry_request: AddEntryRequest) -> str:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        try:
            if add_entry_request.controls is None:
                if add_entry_request.attributes is not None:
                    response = connection.add(add_entry_request.dn, add_entry_request.object_class,
                                              LdapController.scrub_dict(add_entry_request.attributes, True),
                                              add_entry_request.controls)
                else:
                    response = connection.add(add_entry_request.dn, add_entry_request.object_class, None,
                                              add_entry_request.controls)
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

            msg = f'{add_entry_request.dn}: {result_description} {result_message}'

            if result_description == LdapController.success:
                return result_description
            elif result_description == LdapController.entry_already_exists:
                self.logger.warning(msg)
                return msg
            self.logger.error(msg)
            return msg
        finally:
            if connection is not None:
                connection.unbind()

    # This method modifies an existing entry ing LDAP. The dn must match an existing entity.
    def modify(self, server_name: str, modify_entry_request: ModifyEntryRequest) -> str:
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        try:
            changes = modify_entry_request.changes
            for attribute_key in changes:
                attribute = changes[attribute_key]
                temp_dict = {}
                result = []
                for operation in attribute:
                    for operation_key in operation.keys():
                        new_key = LdapController.operation_types[operation_key]
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

            msg = f'{modify_entry_request.dn}: {result_description} {result_message}'
            self.logger.info(msg)
            if result_description == LdapController.success:
                return result_description
            elif result_description == LdapController.insufficient_access_rights:
                self.logger.warning(msg)
            else:
                self.logger.error(msg)
            return msg
        finally:
            if connection is not None:
                connection.unbind()

    def search(self, server_name: str, s: Search) -> SearchResults:
        results = []
        criteria = None
        connection: Connection = self.connection_manager.get_connection(server_name, None)
        try:
            criteria = s.search_filter
            response = connection.search(search_base=s.search_base,
                                         search_filter=s.search_filter,
                                         search_scope=LdapController.search_scope_types[s.search_scope],
                                         dereference_aliases=LdapController.dereference_aliases_types[
                                             s.dereference_aliases],
                                         attributes=LdapController._convert_attributes_keyword(s.attributes),
                                         size_limit=s.size_limit,
                                         time_limit=s.time_limit,
                                         types_only=s.types_only,
                                         get_operational_attributes=s.get_operational_attributes,
                                         controls=s.controls,
                                         paged_size=s.paged_size,
                                         paged_criticality=s.paged_criticality,
                                         paged_cookie=s.paged_cookie)

            if isinstance(response, tuple) and response[1] is not None and 'description' in response[1] and response[1]['description'] == LdapController.success:
                results = self._convert_results(response[2])
            elif connection.result is not None and 'description' in connection.result and connection.result['description'] == LdapController.success:
                results = self._convert_results(connection.entries)

        except Exception as e:
            self.logger.error(e)
        finally:
            if connection is not None:
                connection.unbind()
        return SearchResults(data=results, criteria=criteria)

    def delete(self, server_name: str, dn: Any, controls: Any = None) -> bool:
        connection: Connection = self.connection_manager.get_connection(server_name, None)

        try:
            connection.delete(dn, controls=controls)
        except Exception as e:
            self.logger.warning(f'{dn}  was not deleted. {str(e)}')

        finally:
            if connection is not None:
                connection.unbind()
            return True

    def _convert_results(self, entries: List) -> list:

        results = []
        if entries is not None:
            for entry in entries:
                result = {'dn': None, 'attributes': None}
                if hasattr(entry, 'entry_dn'):
                    result['dn'] = entry.entry_dn
                elif 'dn' in entry:
                    result['dn'] = entry['dn']
                else:
                    self.logger.debug('Cannot find "dn" in entry: ' + str(entry))

                if hasattr(entry, 'entry_attributes_as_dict'):
                    result['attributes'] = entry.entry_attributes_as_dict
                elif 'attributes' in entry:
                    result['attributes'] = dict(entry['attributes'])
                else:
                    self.logger.debug('Cannot find "attributes" in entry: ' + str(entry))
                results.append(result)

        return results

    # This function was added for the health check
    def get_ldap_host(self, server_name) -> str:
        ldap_host: str = self.connection_manager.get_ldap_host(server_name)
        return ldap_host

    def get_ldap_usage(self, server_name: str) -> ConnectionUsage:
        connection: Connection = self.connection_manager.get_connection(server_name)
        return connection.usage

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
