from _typeshed import Incomplete
from webob.compat import MutableMapping

__all__ = ['Cookie', 'CookieProfile', 'SignedCookieProfile', 'SignedSerializer', 'JSONSerializer', 'Base64Serializer', 'make_cookie']

class RequestCookies(MutableMapping):
    def __init__(self, environ) -> None: ...
    def __setitem__(self, name, value) -> None: ...
    def __getitem__(self, name): ...
    def get(self, name, default: Incomplete | None = None): ...
    def __delitem__(self, name) -> None: ...
    def keys(self): ...
    def values(self): ...
    def items(self): ...
    def __contains__(self, name) -> bool: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...

class Cookie(dict):
    def __init__(self, input: Incomplete | None = None) -> None: ...
    def load(self, data) -> None: ...
    def add(self, key, val): ...
    __setitem__ = add
    def serialize(self, full: bool = True): ...
    def values(self): ...

class Morsel(dict):
    name: Incomplete
    value: Incomplete
    def __init__(self, name, value) -> None: ...
    path: Incomplete
    domain: Incomplete
    comment: Incomplete
    expires: Incomplete
    max_age: Incomplete
    httponly: Incomplete
    secure: Incomplete
    samesite: Incomplete
    def __setitem__(self, k, v) -> None: ...
    def serialize(self, full: bool = True): ...

def make_cookie(name, value, max_age: Incomplete | None = None, path: str = '/', domain: Incomplete | None = None, secure: bool = False, httponly: bool = False, comment: Incomplete | None = None, samesite: Incomplete | None = None): ...

class JSONSerializer:
    def dumps(self, appstruct): ...
    def loads(self, bstruct): ...

class Base64Serializer:
    serializer: Incomplete
    def __init__(self, serializer: Incomplete | None = None) -> None: ...
    def dumps(self, appstruct): ...
    def loads(self, bstruct): ...

class SignedSerializer:
    salt: Incomplete
    secret: Incomplete
    hashalg: Incomplete
    salted_secret: Incomplete
    digestmod: Incomplete
    digest_size: Incomplete
    serializer: Incomplete
    def __init__(self, secret, salt, hashalg: str = 'sha512', serializer: Incomplete | None = None) -> None: ...
    def dumps(self, appstruct): ...
    def loads(self, bstruct): ...

class CookieProfile:
    cookie_name: Incomplete
    secure: Incomplete
    max_age: Incomplete
    httponly: Incomplete
    samesite: Incomplete
    path: Incomplete
    domains: Incomplete
    serializer: Incomplete
    request: Incomplete
    def __init__(self, cookie_name, secure: bool = False, max_age: Incomplete | None = None, httponly: Incomplete | None = None, samesite: Incomplete | None = None, path: str = '/', domains: Incomplete | None = None, serializer: Incomplete | None = None) -> None: ...
    def __call__(self, request): ...
    def bind(self, request): ...
    def get_value(self): ...
    def set_cookies(self, response, value, domains=..., max_age=..., path=..., secure=..., httponly=..., samesite=...): ...
    def get_headers(self, value, domains=..., max_age=..., path=..., secure=..., httponly=..., samesite=...): ...

class SignedCookieProfile(CookieProfile):
    secret: Incomplete
    salt: Incomplete
    hashalg: Incomplete
    original_serializer: Incomplete
    def __init__(self, secret, salt, cookie_name, secure: bool = False, max_age: Incomplete | None = None, httponly: bool = False, samesite: Incomplete | None = None, path: str = '/', domains: Incomplete | None = None, hashalg: str = 'sha512', serializer: Incomplete | None = None) -> None: ...
    def bind(self, request): ...
