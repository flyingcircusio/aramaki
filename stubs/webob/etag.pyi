from _typeshed import Incomplete

__all__ = ['AnyETag', 'NoETag', 'ETagMatcher', 'IfRange', 'etag_property']

def etag_property(key, default, rfc_section, strong: bool = True): ...

class _AnyETag:
    def __nonzero__(self): ...
    __bool__ = __nonzero__
    def __contains__(self, other) -> bool: ...

AnyETag: Incomplete

class _NoETag:
    def __nonzero__(self): ...
    __bool__ = __nonzero__
    def __contains__(self, other) -> bool: ...

NoETag: Incomplete

class ETagMatcher:
    etags: Incomplete
    def __init__(self, etags) -> None: ...
    def __contains__(self, other) -> bool: ...
    @classmethod
    def parse(cls, value, strong: bool = True): ...

class IfRange:
    etag: Incomplete
    def __init__(self, etag) -> None: ...
    @classmethod
    def parse(cls, value): ...
    def __contains__(self, resp) -> bool: ...
    def __nonzero__(self): ...
    __bool__ = __nonzero__

class IfRangeDate:
    date: Incomplete
    def __init__(self, date) -> None: ...
    def __contains__(self, resp) -> bool: ...