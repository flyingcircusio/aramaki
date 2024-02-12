import enum
from _typeshed import Incomplete
from collections.abc import Generator
from typing import List, Set, Tuple

def patterns() -> Generator[Incomplete, None, None]: ...
def pytest_assertrepr_compare(op, left, right): ...

class Status(enum.Enum):
    UNEXPECTED: int
    OPTIONAL: int
    EXPECTED: int
    REFUSED: int
    @property
    def symbol(self): ...

STATUS_SYMBOLS: Incomplete
EMPTY_LINE_PATTERN: str

def match(pattern, line): ...

class Line:
    status: Status
    status_cause: str
    data: Incomplete
    def __init__(self, data: str) -> None: ...
    def matches(self, expectation: str): ...
    def mark(self, status: Status, cause: str): ...

class Audit:
    content: List[Line]
    unmatched_expectations: List[Tuple[str, str]]
    matched_refused: Set[Tuple[str, str]]
    def __init__(self, content: str) -> None: ...
    def cursor(self): ...
    def in_order(self, name: str, expected_lines: List[str]): ...
    def optional(self, name: str, tolerated_lines: List[str]): ...
    def refused(self, name: str, refused_lines: List[str]): ...
    def continuous(self, name: str, continuous_lines: List[str]): ...
    def report(self) -> Generator[Incomplete, None, None]: ...
    def is_ok(self): ...

def format_line_report(symbol, cause, line): ...
def pattern_lines(lines: str) -> List[str]: ...

class Pattern:
    name: Incomplete
    library: Incomplete
    ops: Incomplete
    inherited: Incomplete
    def __init__(self, library, name) -> None: ...
    def merge(self, *base_patterns) -> None: ...
    def normalize(self, mode: str): ...
    def continuous(self, lines: str): ...
    def in_order(self, lines: str): ...
    def optional(self, lines: str): ...
    def refused(self, lines: str): ...
    def flat_ops(self) -> Generator[Incomplete, Incomplete, None]: ...
    def __eq__(self, other): ...

class PatternsLib:
    def __getattr__(self, name): ...
