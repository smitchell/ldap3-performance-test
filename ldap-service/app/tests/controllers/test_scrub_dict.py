#!/usr/bin/env python3
from ldap.controllers.ldap_controller import LdapController


def test_scrub_dict_present_value():
    data = {
        'key1': 'A Key',
        'controls': 'control=value'
    }
    result = LdapController.scrub_dict(data)
    assert 'controls' in result, 'Controls were not deleted'


def test_scrub_dict_present_none():
    data = {
        'key1': 'A Key',
        'controls': None
    }
    result = LdapController.scrub_dict(data, True)
    assert 'controls' not in result, 'Controls were not deleted'


def test_scrub_dict_present_none_str():
    data = {
        'key1': 'A Key',
        'controls': 'None'
    }
    result = LdapController.scrub_dict(data, True)
    assert 'controls' not in result, 'Controls were not deleted'


def test_scrub_dict_present_empty():
    data = {
        'key1': 'A Key',
        'controls': ''
    }
    result = LdapController.scrub_dict(data, True)
    assert 'controls' not in result, 'Controls were not deleted'


def test_scrub_dict_do_not_remove_empty():
    data = {
        'key1': 'A Key',
        'controls': ''
    }
    result = LdapController.scrub_dict(data)
    assert 'controls' in result, 'Controls were deleted'
