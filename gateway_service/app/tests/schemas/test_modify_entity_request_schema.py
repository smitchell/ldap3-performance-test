#!/usr/bin/env python3
from api.schemas.modify_entry_request_schema import ModifyEntryRequestSchema

schema = ModifyEntryRequestSchema()


def test_modify_entry_request_load():
    print('test_modify_entry_request_load')
    changeEntityRequestJson = dict(dn='cn=mwatkins,cn=users,cn=employees,ou=test,o=lab',
                                   changes={'mobile': [{'MODIFY_ADD': ['+1 555 555 1862']}]})
    modify_entry_request = schema.load(changeEntityRequestJson)

    assert modify_entry_request.dn == changeEntityRequestJson['dn']
    assert modify_entry_request.changes == changeEntityRequestJson['changes']


def test_modify_entry_request_load_2():
    changeEntityRequestJson = {"dn": "cn=cn=cevans,cn=testing5,ou=test,o=lab",
                               "changes": {"mobile": [{"MODIFY_REPLACE": ["+1 777 777 7777"]}]}}
    modify_entry_request = schema.load(changeEntityRequestJson)

    assert modify_entry_request.dn == changeEntityRequestJson['dn']
    assert modify_entry_request.changes == changeEntityRequestJson['changes']
