#!/usr/bin/env python3
from gateway.dtos.search import Search


def test_create_search_dto():
    search = Search(search_base='cn=cevans,cn=users,cn=employees,ou=test,o=lab',
                    search_filter='(objectClass=organizationalPerson)',
                    search_scope='BASE')
    assert search.search_base == 'cn=cevans,cn=users,cn=employees,ou=test,o=lab', \
        f'Expected cn=cevans,cn=users,cn=employees,ou=test,o=lab but found {search.search_base}'
    assert search.search_filter == '(objectClass=organizationalPerson)', \
        f'Expected (objectClass=organizationalPerson) but found {search.search_filter}'
    assert search.search_scope == 'BASE', f'Expected BASE but found {search.search_scope}'
    assert search.dereference_aliases == 'DEREF_ALWAYS', \
        f'Expected DEREF_ALWAYS but found {search.dereference_aliases}'
    assert search.attributes is None, f'Expected None but found {search.size_limit}'
    assert search.size_limit == 0, f'Expected 0 but found {search.size_limit}'
    assert search.time_limit == 0, f'Expected 0 but found {search.time_limit}'
    assert not search.types_only, f'Expected False but found {search.types_only}'
    assert not search.get_operational_attributes, f'Expected False but found {search.get_operational_attributes}'
    assert search.controls is None, f'Expected None but found {search.controls}'
    assert search.paged_size is None, f'Expected None but found {search.paged_size}'
    assert not search.paged_criticality, f'Expected False but found {search.paged_criticality}'
    assert not search.paged_cookie, f'Expected False but found {search.paged_cookie}'
