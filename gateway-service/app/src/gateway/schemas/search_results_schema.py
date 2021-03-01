#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load

from gateway.dtos.search_results import SearchResults


class SearchResultsSchema(Schema):
    data = fields.List(fields.Dict(), required=False, allow_none=True)
    criteria = fields.Str(required=False, allow_none=True)

    @post_load
    def create(self, data, **kwargs):
        return SearchResults(**data)
