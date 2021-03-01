#!/usr/bin/env python3

from gateway.dtos.add_entry_request import AddEntryRequest


def test_create_add_entry_request_dto():
    print('test_create_add_entry_request_dto')

    attributes = {
            'version': '1',
            'cn': 'Margaret Watkins, Margie Watkins',
            'dn': 'cn=mwatkins,ou=employees,ou=test,o=lab',
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

    add_entry_request = AddEntryRequest('cn=mwatkins,ou=employees,ou=test,o=lab',
                                        'top, person, organizationalPerson, inetOrgPerson', attributes)

    assert add_entry_request.attributes == attributes
