from _typeshed import Incomplete
from pyramid.settings import asbool as asbool, aslist as aslist

class SettingsConfiguratorMixin:
    def add_settings(self, settings: Incomplete | None = None, **kw) -> None: ...
    def get_settings(self): ...

def Settings(d: Incomplete | None = None, _environ_=..., **kw): ...
