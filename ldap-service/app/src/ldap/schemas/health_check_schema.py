#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load

from ldap.dtos.health_check import HealthCheck


class HealthCheckSchema(Schema):
    system = fields.Str(required=True, allow_none=False)
    service_status = fields.Str(allow_none=True)
    hostname = fields.Str(allow_none=True)
    database_host = fields.Str(allow_none=True)
    database_status = fields.Str(allow_none=True)
    ip_addr = fields.Str(allow_none=True)
    date_time = fields.DateTime(allow_none=True)

    @post_load
    def create(self, data, **kwargs):
        return HealthCheck(**data)
