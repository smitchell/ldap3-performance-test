#!/usr/bin/env python3
from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from gateway.dtos.modify_entry_request import ModifyEntryRequest


class ModifyEntryRequestSchema(Schema):
    # {"dn": "cn=cevans,cn=testing5,ou=test,o=lab", "changes": {"mobile": [{"MODIFY_REPLACE": ["+1 777 777 7777"]}]}}
    dn = fields.Str(required=True)
    changes = fields.Dict(
        keys=fields.Str(),  # Attribute Name
        values=fields.List(
            fields.Dict(
                keys=fields.Str(),  # Operation Name
                values=fields.List(
                    fields.Str()  # Values
                )
            )
        ), required=True)
    controls = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True, default=None)

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        return ModifyEntryRequest(**data)
