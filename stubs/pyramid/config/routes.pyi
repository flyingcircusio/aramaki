from _typeshed import Incomplete
from collections.abc import Generator
from pyramid.config.actions import action_method as action_method
from pyramid.config.predicates import normalize_accept_offer as normalize_accept_offer, predvalseq as predvalseq
from pyramid.exceptions import ConfigurationError as ConfigurationError
from pyramid.interfaces import IRequest as IRequest, IRouteRequest as IRouteRequest, IRoutesMapper as IRoutesMapper, PHASE2_CONFIG as PHASE2_CONFIG
from pyramid.request import route_request_iface as route_request_iface
from pyramid.urldispatch import RoutesMapper as RoutesMapper
from pyramid.util import as_sorted_tuple as as_sorted_tuple, is_nonstr_iter as is_nonstr_iter

class RoutesConfiguratorMixin:
    def add_route(self, name, pattern: Incomplete | None = None, factory: Incomplete | None = None, for_: Incomplete | None = None, header: Incomplete | None = None, xhr: Incomplete | None = None, accept: Incomplete | None = None, path_info: Incomplete | None = None, request_method: Incomplete | None = None, request_param: Incomplete | None = None, traverse: Incomplete | None = None, custom_predicates=(), use_global_views: bool = False, path: Incomplete | None = None, pregenerator: Incomplete | None = None, static: bool = False, inherit_slash: Incomplete | None = None, **predicates): ...
    def add_route_predicate(self, name, factory, weighs_more_than: Incomplete | None = None, weighs_less_than: Incomplete | None = None) -> None: ...
    def add_default_route_predicates(self) -> None: ...
    def get_routes_mapper(self): ...
    route_prefix: Incomplete
    def route_prefix_context(self, route_prefix) -> Generator[None, None, None]: ...
