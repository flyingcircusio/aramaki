from _typeshed import Incomplete
from collections.abc import Iterable as Iterable
from html.entities import name2codepoint as name2codepoint
from http import cookies
from urllib.parse import urlencode as urlencode

SimpleCookie = cookies.SimpleCookie
CookieError = cookies.CookieError

def to_bytes(value, charset: str = 'latin1'): ...
def print_stderr(value) -> None: ...
def escape_cookie_value(value): ...

COOKIE_ESCAPE_CHAR_MAP: Incomplete
