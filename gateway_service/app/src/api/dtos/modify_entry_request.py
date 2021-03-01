#!/usr/bin/env python3
class ModifyEntryRequest:

    def __init__(self, dn: str, changes: list, controls: list = None):
        self.dn = dn
        self.changes = changes
        self.controls = controls
