#!/usr/bin/env python3

from gateway.schemas.add_entry_request_schema import AddEntryRequestSchema

schema = AddEntryRequestSchema()

data = {
    'dn': 'cn=mwatkins,ou=employees,ou=test,o=lab',
    'object_class': ['person','organizationalPerson','inetOrgPerson'],
    'attributes': {
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
}


def test_add_entry_request_load():
    print('test_add_entry_request_load')

    add_entry_request = schema.load(data)

    assert add_entry_request.dn == data['dn']
    assert add_entry_request.object_class == data['object_class']


def test_add_entry_request_dump():
    print('test_add_entry_request_dump')

    output = schema.dump(schema.load(data))

    assert output is not None
    assert output['dn'] == data['dn']
    assert output['object_class'] == data['object_class']
    assert output['attributes'] == data['attributes']
