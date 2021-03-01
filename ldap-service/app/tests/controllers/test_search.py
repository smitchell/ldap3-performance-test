#!/usr/bin/env python3
from ldap.controllers.connection_manager import ConnectionManager
from ldap.controllers.ldap_controller import LdapController
from ldap.dtos.search_results import SearchResults
from ldap.schemas.add_entry_request_schema import AddEntryRequestSchema
from ldap.schemas.search_schema import SearchSchema

schema = AddEntryRequestSchema()
connection_manager = ConnectionManager()
attributes = {
    'cn': 'Charles Evans, Chuck Evans',
    'dn': 'cn=cevans,cn=users,cn=employees,ou=test,o=lab',
    'o': 'lab',
    'ou': 'test',
    'sn': 'evans',
    'uid': 'cevans',
    'givenName': 'charles',
    'initials': 'CPE',
    'displayName': 'Chuck Evans',
    'telephoneNumber': '+1 408 555 3433',
    'homePhone': '+1 555 555 3532',
    'mobile': '+1 555 555 3375',
    'userPassword': '123password',
    'employeeNumber': 'mpw-6453',
    'employeeType': 'full time',
    'preferredLanguage': 'en-US',
    'mail': 'mwatkins@company.com',
    'title': 'consultant, senior consultant',
    'labeledURI': 'http://www.comapny.com/users/cevans My Home Page'
}
mocked_name = 'mocked'

def test_search_ou_by_dn():

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    result = controller.add(mocked_name, add_entry_request)
    dn = add_entry_request.dn
    assert result, f'There was a problem adding {dn}'

    search_data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'BASE'
    }
    search_schema = SearchSchema()
    search_results: SearchResults = controller.search(mocked_name, search_schema.load(search_data))
    assert search_results is not None
    assert len(search_results.data) == 1, f'Expect one search result but found {len(search_results.data)}'
    for entry in search_results.data:
        assert entry['dn'] == dn, f'Expected {dn} but found {entry["dn"]}'


def test_search_person_by_dn():

    # Pass the new employees data to the controller
    controller = LdapController()
    add_entry_request = schema.load({
        'dn': 'cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    controller.add(mocked_name, add_entry_request)

    add_entry_request = schema.load({
        'dn': 'cn=users,cn=employees,ou=test,o=lab',
        'object_class': 'organizationalUnit'
    })
    controller.add(mocked_name, add_entry_request)

    add_entry_request = schema.load({
        'dn': 'cn=cevans,cn=users,cn=employees,ou=test,o=lab',
        'object_class': ['person', 'organizationalPerson', 'inetOrgPerson'],
        'attributes': attributes
    })
    controller.add(mocked_name, add_entry_request)

    search_data = {
        'search_base': add_entry_request.dn,
        'search_filter': '(objectClass=organizationalPerson)',
        'search_scope': 'BASE'
    }
    search_schema = SearchSchema()
    search_results: SearchResults = controller.search(mocked_name, search_schema.load(search_data))
    assert search_results is not None
    assert len(search_results.data) == 1, f'Expect one search result but found {len(search_results.data)}'
    for entry in search_results.data:
        assert entry['dn'] == add_entry_request.dn, f'Expected {add_entry_request.dn} but found {entry["dn"]}'
