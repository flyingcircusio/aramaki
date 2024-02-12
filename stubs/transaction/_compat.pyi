from _typeshed import Incomplete
from io import StringIO as StringIO

PY3: Incomplete
JYTHON: Incomplete
text_type = str

def text_(s): ...
def native_(s, encoding: str = 'latin-1', errors: str = 'strict'): ...
def reraise(tp, value, tb: Incomplete | None = None) -> None: ...
