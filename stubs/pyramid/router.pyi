from _typeshed import Incomplete
from pyramid.events import BeforeTraversal as BeforeTraversal, ContextFound as ContextFound, NewRequest as NewRequest, NewResponse as NewResponse
from pyramid.httpexceptions import HTTPNotFound as HTTPNotFound
from pyramid.interfaces import IDebugLogger as IDebugLogger, IExecutionPolicy as IExecutionPolicy, IRequest as IRequest, IRequestExtensions as IRequestExtensions, IRequestFactory as IRequestFactory, IRootFactory as IRootFactory, IRouteRequest as IRouteRequest, IRouter as IRouter, IRoutesMapper as IRoutesMapper, ITraverser as ITraverser, ITweens as ITweens
from pyramid.request import Request as Request, apply_request_extensions as apply_request_extensions
from pyramid.threadlocal import RequestContext as RequestContext
from pyramid.traversal import DefaultRootFactory as DefaultRootFactory, ResourceTreeTraverser as ResourceTreeTraverser

class Router:
    debug_notfound: bool
    debug_routematch: bool
    logger: Incomplete
    root_factory: Incomplete
    routes_mapper: Incomplete
    request_factory: Incomplete
    request_extensions: Incomplete
    execution_policy: Incomplete
    orig_handle_request: Incomplete
    root_policy: Incomplete
    registry: Incomplete
    def __init__(self, registry) -> None: ...
    def handle_request(self, request): ...
    def invoke_subrequest(self, request, use_tweens: bool = False): ...
    def request_context(self, environ): ...
    def invoke_request(self, request, _use_tweens: bool = True): ...
    def finish_request(self, request) -> None: ...
    def __call__(self, environ, start_response): ...

def default_execution_policy(environ, router): ...
