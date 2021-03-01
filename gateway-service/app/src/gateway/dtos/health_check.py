#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime


class HealthCheck:

    def __init__(self,
                 system: str,
                 hostname: str = None,
                 ip_addr: str = None,
                 status: str = 'OK'):
        self.system = system
        self.status = status
        self.hostname = hostname
        self.ip_addr = ip_addr
