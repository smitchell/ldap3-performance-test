#!/usr/bin/env python3
import json
from typing import Optional

from flask import current_app
from ldap3 import Server, Connection, ServerPool, ROUND_ROBIN

from api.app import app


class ConnectionManager:
    mocked = 'mocked'
    mocked_server = None
    mocked_config: dict = {}
    server_pools = {}
    ldap_configs: dict = {}


    def __init__(self):
        with app.app_context():
            self.logger = current_app.logger
            self.mocked_config: dict = current_app.config['ldap_mocked']
            self.ldap_configs = app.config['ldap_servers']
            self.mocked_server = Server(self.mocked_config['ldap_host'], **self.mocked_config['server_config'])
            # This example came from an env where there are multiple replicated named LDAP groups
            for server_name in self.ldap_configs.keys():
                self.server_pools[server_name] = self.build_server_pool(server_name)

    def build_server_pool(self, server_name: str) -> ServerPool:
        server_config = self.ldap_configs[server_name]['server_config']
        """
        Read the server pool docs: https://ldap3.readthedocs.io/en/latest/server.html
        """
        server_pool = ServerPool(None, ROUND_ROBIN, active=True, exhaust=30)
        server_pool.add(Server(self.ldap_configs[server_name]['ldap_host'], **server_config))
        return server_pool

    def get_mocked_connection(self) -> Connection:
        """
        The mocked connection is heavy weight, as it loads the CHS server and schema info for better testing.
        You need to update mocked_server_schema.json if the CHS schema changes
        See https://ldap3.readthedocs.io/en/latest/server.html#offline-schema
        """
        connection_config = self.mocked_config['connection_config']
        conn = Connection(self.mocked_server, **connection_config)
        if not connection_config['auto_bind']:
            conn.bind()
        elif conn.closed:
            conn.open()
        return conn


    def get_connection(self, server_name: str, params: dict = None):
        """
        Creates a connection using the mocked server, for unit tests, or a server pool.
        """
        if server_name == self.mocked:
            return self.get_mocked_connection()

        if server_name not in self.server_pools:
            self.logger.warning(f'{server_name} not found in server pools')
        default_connection_config = self.ldap_configs[server_name]['connection_config']
        connection_config = default_connection_config.copy()
        if params is not None:
            connection_config.update(params)
        conn = Connection(self.server_pools[server_name], **connection_config)
        return conn
