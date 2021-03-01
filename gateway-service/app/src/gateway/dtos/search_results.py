#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class SearchResults:

    def __init__(self, data=None, criteria=None):
        if data is None:
            data = []
        self.data = data
        self.criteria = criteria
