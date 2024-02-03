import inspect
import venusian
from _typeshed import Incomplete
from pyramid.asset import resolve_asset_spec as resolve_asset_spec
from pyramid.authorization import ACLAuthorizationPolicy as ACLAuthorizationPolicy
from pyramid.config.actions import ActionConfiguratorMixin as ActionConfiguratorMixin, ActionState as ActionState, action_method as action_method
from pyramid.config.adapters import AdaptersConfiguratorMixin as AdaptersConfiguratorMixin
from pyramid.config.assets import AssetsConfiguratorMixin as AssetsConfiguratorMixin
from pyramid.config.factories import FactoriesConfiguratorMixin as FactoriesConfiguratorMixin
from pyramid.config.i18n import I18NConfiguratorMixin as I18NConfiguratorMixin
from pyramid.config.predicates import PredicateConfiguratorMixin as PredicateConfiguratorMixin, not_ as not_
from pyramid.config.rendering import RenderingConfiguratorMixin as RenderingConfiguratorMixin
from pyramid.config.routes import RoutesConfiguratorMixin as RoutesConfiguratorMixin
from pyramid.config.security import SecurityConfiguratorMixin as SecurityConfiguratorMixin
from pyramid.config.settings import SettingsConfiguratorMixin as SettingsConfiguratorMixin
from pyramid.config.testing import TestingConfiguratorMixin as TestingConfiguratorMixin
from pyramid.config.tweens import TweensConfiguratorMixin as TweensConfiguratorMixin
from pyramid.config.views import ViewsConfiguratorMixin as ViewsConfiguratorMixin
from pyramid.config.zca import ZCAConfiguratorMixin as ZCAConfiguratorMixin
from pyramid.events import ApplicationCreated as ApplicationCreated
from pyramid.exceptions import ConfigurationError as ConfigurationError
from pyramid.httpexceptions import default_exceptionresponse_view as default_exceptionresponse_view
from pyramid.interfaces import IDebugLogger as IDebugLogger, IExceptionResponse as IExceptionResponse, PHASE0_CONFIG as PHASE0_CONFIG, PHASE1_CONFIG as PHASE1_CONFIG, PHASE2_CONFIG as PHASE2_CONFIG, PHASE3_CONFIG as PHASE3_CONFIG
from pyramid.path import DottedNameResolver as DottedNameResolver, caller_package as caller_package, package_of as package_of
from pyramid.registry import Introspectable as Introspectable, Introspector as Introspector, Registry as Registry
from pyramid.router import Router as Router
from pyramid.settings import aslist as aslist
from pyramid.threadlocal import manager as manager
from pyramid.util import WeakOrderedSet as WeakOrderedSet, get_callable_name as get_callable_name, object_description as object_description

not_ = not_
PHASE0_CONFIG = PHASE0_CONFIG
PHASE1_CONFIG = PHASE1_CONFIG
PHASE2_CONFIG = PHASE2_CONFIG
PHASE3_CONFIG = PHASE3_CONFIG
ActionState = ActionState

class Configurator(ActionConfiguratorMixin, PredicateConfiguratorMixin, TestingConfiguratorMixin, TweensConfiguratorMixin, SecurityConfiguratorMixin, ViewsConfiguratorMixin, RoutesConfiguratorMixin, ZCAConfiguratorMixin, I18NConfiguratorMixin, RenderingConfiguratorMixin, AssetsConfiguratorMixin, SettingsConfiguratorMixin, FactoriesConfiguratorMixin, AdaptersConfiguratorMixin):
    manager = manager
    venusian = venusian
    basepath: Incomplete
    includepath: Incomplete
    info: str
    object_description: Incomplete
    introspectable = Introspectable
    inspect = inspect
    name_resolver: Incomplete
    package_name: Incomplete
    package: Incomplete
    root_package: Incomplete
    registry: Incomplete
    autocommit: Incomplete
    route_prefix: Incomplete
    introspection: Incomplete
    def __init__(self, registry: Incomplete | None = None, package: Incomplete | None = None, settings: Incomplete | None = None, root_factory: Incomplete | None = None, security_policy: Incomplete | None = None, authentication_policy: Incomplete | None = None, authorization_policy: Incomplete | None = None, renderers: Incomplete | None = None, debug_logger: Incomplete | None = None, locale_negotiator: Incomplete | None = None, request_factory: Incomplete | None = None, response_factory: Incomplete | None = None, default_permission: Incomplete | None = None, session_factory: Incomplete | None = None, default_view_mapper: Incomplete | None = None, autocommit: bool = False, exceptionresponse_view=..., route_prefix: Incomplete | None = None, introspection: bool = True, root_package: Incomplete | None = None) -> None: ...
    def setup_registry(self, settings: Incomplete | None = None, root_factory: Incomplete | None = None, security_policy: Incomplete | None = None, authentication_policy: Incomplete | None = None, authorization_policy: Incomplete | None = None, renderers: Incomplete | None = None, debug_logger: Incomplete | None = None, locale_negotiator: Incomplete | None = None, request_factory: Incomplete | None = None, response_factory: Incomplete | None = None, default_permission: Incomplete | None = None, session_factory: Incomplete | None = None, default_view_mapper: Incomplete | None = None, exceptionresponse_view=...) -> None: ...
    introspector: Incomplete
    def include(self, callable, route_prefix: Incomplete | None = None) -> None: ...
    def add_directive(self, name, directive, action_wrap: bool = True) -> None: ...
    def __getattr__(self, name): ...
    def with_package(self, package): ...
    def maybe_dotted(self, dotted): ...
    def absolute_asset_spec(self, relative_spec): ...
    absolute_resource_spec = absolute_asset_spec
    def begin(self, request=...) -> None: ...
    def end(self): ...
    def __enter__(self): ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: types.TracebackType | None) -> None: ...
    def scan(self, package: Incomplete | None = None, categories=('pyramid',), onerror: Incomplete | None = None, ignore: Incomplete | None = None, **kw) -> None: ...
    def make_wsgi_app(self): ...

global_registries: Incomplete
