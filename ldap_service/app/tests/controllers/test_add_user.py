#!/usr/bin/env python3
from api.controllers.connection_manager import ConnectionManager
from api.controllers.ldap_controller import LdapController
from api.dtos.search_results import SearchResults
from api.schemas.add_entry_request_schema import AddEntryRequestSchema
from api.schemas.search_schema import SearchSchema

schema = AddEntryRequestSchema()
connection_manager = ConnectionManager()
attributes = {
    'cn': 'Margaret Watkins, Margie Watkins',
    'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
    'o': 'lab',
    'ou': 'test',
    'sn': 'Watkins',
    'uid': 'mwatkins',
    'givenName': 'Margaret',
    'initials': 'MPW',
    'displayName': 'Margie Watkins',
    'telephoneNumber': '+1 408 555 1862',
    'homePhone': '+1 555 555 1862',
    'mobile': '+1 555 555 1862',
    'userPassword': '123password',
    'employeeNumber': 'mpw-3948',
    'employeeType': 'full time',
    'preferredLanguage': 'en-US',
    'mail': 'mwatkins@company.com',
    'title': 'consultant, senior consultant',
    'labeledURI': 'http://www.comapny.com/users/mwatkins My Home Page'
}
mocked_name = 'mocked'


def test_add_user_with_controller():

    # Build out the fake organization
    controller = LdapController()

    add_entry_request = schema.load({'dn': 'cn=employees,ou=test,o=lab', 'object_class': 'organizationalUnit'})
    controller.add(mocked_name, add_entry_request)
    add_entry_request = schema.load({'dn': 'cn=users,cn=employees,ou=test,o=lab', 'object_class': 'organizationalUnit'})
    controller.add(mocked_name, add_entry_request)

    # Pass the new user data to the controller

    add_entry_request = schema.load({
        'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
        'object_class': ['top,person', 'organizationalPerson', 'inetOrgPerson'],
        'attributes': attributes
    })
    result = controller.add(mocked_name, add_entry_request)
    assert result, 'There was a problem adding the user'
    dn = add_entry_request.dn

    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalPerson)',
        'attributes': 'ALL_ATTRIBUTES'
    }
    search_schema = SearchSchema()
    search_results: SearchResults = controller.search(mocked_name, search_schema.load(data))
    total_results = len(search_results.data)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'
