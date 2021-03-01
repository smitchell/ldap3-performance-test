from typing import Any

class Search:

    def __init__(self, search_base,
                 search_filter: str,
                 search_scope: str = 'SUBTREE',
                 dereference_aliases: str = 'DEREF_ALWAYS',
                 attributes: Any = None,
                 size_limit: int = 0,
                 time_limit: int = 0,
                 types_only: bool = False,
                 get_operational_attributes: bool = False,
                 controls: Any = None,
                 paged_size: int = None,
                 paged_criticality: bool = False,
                 paged_cookie: Any = None):
        self.search_base = search_base
        self.search_filter = search_filter
        self.search_scope = search_scope
        self.dereference_aliases = dereference_aliases
        self.attributes = attributes
        self.size_limit = size_limit
        self.time_limit = time_limit
        self.types_only = types_only
        self.get_operational_attributes = get_operational_attributes
        self.controls = controls
        self.paged_size = paged_size
        self.paged_criticality = paged_criticality
        self.paged_cookie = paged_cookie
