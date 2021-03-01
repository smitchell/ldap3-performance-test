#!/usr/bin/env python3
from api.schemas.search_schema import SearchSchema

schema = SearchSchema()

data = {
    'search_base': 'cn=cevans,cn=users,cn=employees,ou=test,o=lab',
    'search_filter': '(objectClass=organizationalPerson)',
    'search_scope': 'BASE'
}


def test_search_load():
    print('test_search_load')

    search = schema.load(data)

    assert search.search_base == data['search_base'], f'Expected {data["search_base"]} but found {search.search_base}'
    assert search.search_filter == data[
        'search_filter'], f'Expected {data["search_filter"]} but found {search.search_filter}'
    assert search.search_scope == data[
        'search_scope'], f'Expected {data["search_scope"]} but found {search.search_scope}'
    assert search.dereference_aliases == 'DEREF_ALWAYS', f'Expected DEREF_ALWAYS but found {search.dereference_aliases}'
    assert search.attributes is None, f'Expected None but found {search.attributes}'
    assert search.size_limit == 0, f'Expected 0 but found {search.size_limit}'
    assert search.time_limit == 0, f'Expected 0 but found {search.time_limit}'
    assert not search.types_only, f'Expected False but found {search.types_only}'
    assert not search.get_operational_attributes, f'Expected False but found {search.get_operational_attributes}'
    assert search.controls is None, f'Expected None but found {search.controls}'
    assert search.paged_size is None, f'Expected None but found {search.paged_size}'
    assert not search.paged_criticality, f'Expected False but found {search.paged_criticality}'
    assert not search.paged_cookie, f'Expected False but found {search.paged_cookie}'


def test_search_dump():
    print('test_search_dump')

    search = schema.dump(schema.load(data))

    assert search['search_base'] == data[
        'search_base'], f'Expected {data["search_base"]} but found {search["search_base"]}'
    assert search['search_filter'] == data[
        'search_filter'], f'Expected {data["search_filter"]} but found {search["search_filter"]}'
    assert search['search_scope'] == data[
        'search_scope'], f'Expected {data["search_scope"]} but found {search["search_scope"]}'
    assert search['dereference_aliases'] == 'DEREF_ALWAYS', \
        f'Expected DEREF_ALWAYS but found {search["dereference_aliases"]}'
    assert search['attributes'] is None, f'Expected None but found {search["attributes"]}'
    assert search['size_limit'] == 0, f'Expected 0 but found {search["size_limit"]}'
    assert search['time_limit'] == 0, f'Expected 0 but found {search["time_limit"]}'
    assert not search['types_only'], f'Expected False but found {search["types_only"]}'
    assert not search['get_operational_attributes'], f'Expected False but found {search["get_operational_attributes"]}'
    assert search['controls'] is None, f'Expected None but found {search["controls"]}'
    assert search['paged_size'] is None, f'Expected None but found {search["paged_size"]}'
    assert not search['paged_criticality'], f'Expected False but found {search["paged_criticality"]}'
    assert not search['paged_cookie'], f'Expected False but found {search["paged_cookie"]}'
