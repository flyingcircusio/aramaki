from _typeshed import Incomplete
from pyramid.config import global_registries as global_registries
from pyramid.exceptions import ConfigurationError as ConfigurationError
from pyramid.interfaces import IRequestFactory as IRequestFactory, IRootFactory as IRootFactory
from pyramid.request import Request as Request, apply_request_extensions as apply_request_extensions
from pyramid.threadlocal import RequestContext as RequestContext
from pyramid.traversal import DefaultRootFactory as DefaultRootFactory

def get_root(app, request: Incomplete | None = None): ...
def prepare(request: Incomplete | None = None, registry: Incomplete | None = None): ...

class AppEnvironment(dict):
    def __enter__(self): ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
