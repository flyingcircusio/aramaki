from _typeshed import Incomplete
from pyramid.httpexceptions import HTTPBadRequest as HTTPBadRequest, HTTPForbidden as HTTPForbidden, HTTPNotFound as HTTPNotFound

NotFound = HTTPNotFound
Forbidden = HTTPForbidden

class BadCSRFOrigin(HTTPBadRequest):
    title: str
    explanation: str

class BadCSRFToken(HTTPBadRequest):
    title: str
    explanation: str

class PredicateMismatch(HTTPNotFound): ...
class URLDecodeError(UnicodeDecodeError): ...
class ConfigurationError(Exception): ...

class ConfigurationConflictError(ConfigurationError):
    def __init__(self, conflicts) -> None: ...

class ConfigurationExecutionError(ConfigurationError):
    def __init__(self, etype, evalue, info) -> None: ...

class CyclicDependencyError(Exception):
    cycles: Incomplete
    def __init__(self, cycles) -> None: ...
