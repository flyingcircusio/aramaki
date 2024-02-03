from Queue import Empty as Empty, Queue as Queue
from _typeshed import Incomplete
from cgi import FieldStorage as _cgi_FieldStorage
from collections import Iterable as Iterable, MutableMapping as MutableMapping
from collections.abc import Generator
from html import escape as escape
from urllib import parse
from urllib.parse import quote_plus as quote_plus

PY3: Incomplete
PY2: Incomplete
string_types: Incomplete
integer_types: Incomplete
class_types: Incomplete
text_type = str
long = int

def text_(s, encoding: str = 'latin-1', errors: str = 'strict'): ...
def bytes_(s, encoding: str = 'latin-1', errors: str = 'strict'): ...
def native_(s, encoding: str = 'latin-1', errors: str = 'strict'): ...
urlparse = parse

def reraise(exc_info) -> None: ...
def iteritems_(d): ...
def itervalues_(d): ...
def unquote(string): ...
def url_unquote(s): ...
def parse_qsl_text(qs, encoding: str = 'utf-8') -> Generator[Incomplete, None, None]: ...

class cgi_FieldStorage(_cgi_FieldStorage):
    def make_file(self): ...
    list: Incomplete
    def read_multi(self, environ, keep_blank_values, strict_parsing) -> None: ...
