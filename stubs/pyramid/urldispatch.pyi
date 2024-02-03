from _typeshed import Incomplete
from pyramid.exceptions import URLDecodeError as URLDecodeError
from pyramid.interfaces import IRoute as IRoute, IRoutesMapper as IRoutesMapper
from pyramid.traversal import PATH_SAFE as PATH_SAFE, quote_path_segment as quote_path_segment, split_path_info as split_path_info
from pyramid.util import is_nonstr_iter as is_nonstr_iter, text_ as text_

class Route:
    pattern: Incomplete
    path: Incomplete
    name: Incomplete
    factory: Incomplete
    predicates: Incomplete
    pregenerator: Incomplete
    def __init__(self, name, pattern, factory: Incomplete | None = None, predicates=(), pregenerator: Incomplete | None = None) -> None: ...

class RoutesMapper:
    routelist: Incomplete
    static_routes: Incomplete
    routes: Incomplete
    def __init__(self) -> None: ...
    def has_routes(self): ...
    def get_routes(self, include_static: bool = False): ...
    def get_route(self, name): ...
    def connect(self, name, pattern, factory: Incomplete | None = None, predicates=(), pregenerator: Incomplete | None = None, static: bool = False): ...
    def generate(self, name, kw): ...
    def __call__(self, request): ...

old_route_re: Incomplete
star_at_end: Incomplete
route_re: Incomplete

def update_pattern(matchobj): ...
