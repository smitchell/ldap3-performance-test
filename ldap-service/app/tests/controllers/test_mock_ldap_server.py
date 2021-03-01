#!/usr/bin/env python3
from ldap3 import Server, Connection, MOCK_SYNC, ALL_ATTRIBUTES, BASE
from ldap.schemas.add_entry_request_schema import AddEntryRequestSchema

server = Server('my_fake_server')
schema = AddEntryRequestSchema()

attributes = {
    'cn': 'Margaret Watkins, Margie Watkins',
    'dn': 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
    'o': 'lab',
    'ou': 'test',
    'sn': 'Watkins',
    'uid': 'mwatkins',
    'objectClass': ['person', 'organizationalPerson', 'inetOrgPerson'],
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


def test_direct_add_with_mocked_date():

    connection = Connection(server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)
    connection.bind()

    dn = 'cn=employees,ou=test,o=lab'
    connection.add(dn, 'organizationalUnit')
    result_description = connection.result["description"]
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}. {connection.last_error}'
    print(f'Successfully added {dn}')

    dn = 'cn=users,cn=employees,ou=test,o=lab'
    connection.add(dn, 'organizationalUnit')
    result_description = connection.result["description"]
    assert result_description == 'success', f'Add {dn} failed.{result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}. {connection.last_error}'
    print(f'Successfully added {dn}')

    dn = 'cn=mwatkins,cn=users,cn=employees,ou=test,o=lab'

    connection.add(dn, ['person', 'organizationalPerson', 'inetOrgPerson'], attributes)
    result_description = connection.result["description"]
    assert result_description == 'success', f'Add {dn} failed. {result_description}'
    assert connection.last_error is None, f'An error occurred adding {dn}. {connection.last_error}'

    connection.search(search_base=dn, search_filter='(objectClass=*)', search_scope=BASE, attributes=ALL_ATTRIBUTES)
    result_description = connection.result["description"]
    assert result_description == 'success', f'Searching for {dn} failed. {result_description}'
    assert connection.last_error is None, f'An error occurred searching for {dn}. {connection.last_error}'
    total_results = len(connection.entries)
    assert total_results == 1, f'Expected 1 search result for {dn} but found {total_results}'
