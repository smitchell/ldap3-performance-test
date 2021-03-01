#!/usr/bin/env python3
from ldap.controllers.connection_manager import ConnectionManager
from ldap.controllers.ldap_controller import LdapController
from ldap.dtos.search_results import SearchResults
from ldap.schemas.search_schema import SearchSchema

connection_manager = ConnectionManager()
controller = LdapController()
search_schema = SearchSchema()
mocked_name = 'mocked'


def test_delete_bad_dn():
    assert controller.delete(mocked_name, "doogie")


def test_delete_good_dn():
    dn = 'cn=random_cn,cn=groups,ou=test,o=lab'
    connection = connection_manager.get_connection(mocked_name)
    return_value = connection.add(dn, object_class='organizationalUnit')
    assert return_value

    data = {
        'search_base': dn,
        'search_filter': '(objectClass=organizationalUnit)',
        'search_scope': 'BASE',
        'attributes': 'ALL_ATTRIBUTES'
    }

    assert controller.delete(mocked_name, dn)

    search_results: SearchResults = controller.search(mocked_name, search_schema.load(data))
    assert len(search_results.data) == 0, f'AFTER: Expected 1 search result but found {search_results.data}'
