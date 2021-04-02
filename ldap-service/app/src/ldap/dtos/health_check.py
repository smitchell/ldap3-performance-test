#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime


class HealthCheck:

    def __init__(self,
                 system: str,
                 hostname: str = None,
                 ip_addr: str = None,
                 database_host: str = None,
                 database_status: str = None,
                 service_status: str = 'OK'):
        self.system = system
        self.service_status = service_status
        self.hostname = hostname
        self.database_host = database_host
        self.database_status = database_status
        self.ip_addr = ip_addr
