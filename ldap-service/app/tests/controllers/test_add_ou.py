#!/usr/bin/env python3
from ldap.controllers.connection_manager import ConnectionManager
from ldap.controllers.ldap_controller import LdapController
from ldap.dtos.search_results import SearchResults
from ldap.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap.schemas.search_schema import SearchSchema

schema = AddEntryRequestSchema()
connection_manager = ConnectionManager()
mocked_name = 'mocked'

def test_add_user_with_controller():

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit',
        'attributes': None,
        'controls': None
    })
    result = controller.add(mocked_name, add_entry_request)
    assert result, 'There was a problem adding {add_entry_request.dn}'

    dn = add_entry_request.dn
    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'SUBTREE'
    }
    search_schema = SearchSchema()
    search_results: SearchResults = controller.search(mocked_name, search_schema.load(data))
    total_results = len(search_results.data)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'

    add_entry_request = schema.load({
        'dn': 'cn=users,cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })

    result = controller.add(mocked_name, add_entry_request)
    dn = add_entry_request.dn
    assert result, 'There was a problem adding {dn}'

    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'SUBTREE'
    }
    search_schema = SearchSchema()
    search_results: SearchResults = controller.search(mocked_name, search_schema.load(data))
    total_results = len(search_results.data)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'
