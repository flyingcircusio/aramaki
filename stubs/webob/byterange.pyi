from _typeshed import Incomplete

__all__ = ['Range', 'ContentRange']

class Range:
    start: Incomplete
    end: Incomplete
    def __init__(self, start, end) -> None: ...
    def range_for_length(self, length): ...
    def content_range(self, length): ...
    def __iter__(self): ...
    @classmethod
    def parse(cls, header): ...

class ContentRange:
    start: Incomplete
    stop: Incomplete
    length: Incomplete
    def __init__(self, start, stop, length) -> None: ...
    def __iter__(self): ...
    @classmethod
    def parse(cls, value): ...
