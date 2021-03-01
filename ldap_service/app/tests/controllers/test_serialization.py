import json

from requests.structures import CaseInsensitiveDict

data: dict = {'data': [{'dn': 'uid=john,ou=people,dc=byteworks,dc=com', 'attributes': {'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'], 'cn': ['John Doe'], 'uid': ['john']}}, {'dn': 'uid=jane,ou=people,dc=byteworks,dc=com', 'attributes': {'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'], 'cn': ['Jane Doe'], 'uid': ['jane']}}]}

def test_serialize_dict():
    caseInsensitiveDict = CaseInsensitiveDict(data)
    serialized_data = json.dumps(dict(caseInsensitiveDict))
    assert serialized_data is not None
