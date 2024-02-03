from _typeshed import Incomplete
from pyramid import renderers as renderers
from pyramid.config.actions import action_method as action_method
from pyramid.interfaces import IRendererFactory as IRendererFactory, PHASE1_CONFIG as PHASE1_CONFIG

DEFAULT_RENDERERS: Incomplete

class RenderingConfiguratorMixin:
    def add_default_renderers(self) -> None: ...
    def add_renderer(self, name, factory) -> None: ...
