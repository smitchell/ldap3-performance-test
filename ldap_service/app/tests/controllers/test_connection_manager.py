#!/usr/bin/env python3
from collections import OrderedDict

from ldap3 import Server, Connection

from api.app import app
from api.controllers.connection_manager import ConnectionManager

data: OrderedDict = OrderedDict(
    [('ldap_servers', OrderedDict([('test', OrderedDict(
        [('ldap_host', '192.168.1.5'),
         ('server_config', OrderedDict(
             [
                 ('port', 389),
                 ('connect_timeout', 30)
             ])),
         ('connection_config', OrderedDict(
             [('auto_bind', 'AUTO_BIND_NO_TLS'),
              ('user', 'admin'),
              ('password', 'abadpassword'),
              ('authentication', 'SIMPLE'),
              ('client_strategy', 'REUSABLE')
              ]))
         ])),
                                   ('mocked', OrderedDict(
                                       [('ldap_host', 'localhost'),
                                        ('server_config', OrderedDict([('port', 389)])),
                                        ('connection_config', OrderedDict(
                                            [('user', 'admin'), ('password', 'abadpassword'),
                                             ('client_strategy', 'MOCK_SYNC')
                                             ]))
                                        ]))
                                   ]))
     ])

connection_manager = ConnectionManager()
app.config['ldap_servers'] = data['ldap_servers']

def test_server_connection_config():
    config = connection_manager.ldap_configs['test']['connection_config']
    assert config is not None, 'Expected mocked config, but found none'

    actual = config['client_strategy']
    expected = 'SYNC'
    assert actual == expected, f'Expected {expected} but found {actual}'

    actual = config['authentication']
    expected = 'SIMPLE'
    assert actual == expected, f'Expected {expected} but found {actual}'


def test_connection_manager_get_connection():
    connection: Connection = connection_manager.get_connection('mocked', None)
    assert connection is not None, 'Expected a Connection, but found none.'
