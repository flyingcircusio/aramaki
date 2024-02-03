from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['AdapterRegistry', 'VerifyingAdapterRegistry']

class BaseAdapterRegistry:
    __bases__: Incomplete
    def __init__(self, bases=()) -> None: ...
    def changed(self, originally_changed) -> None: ...
    def register(self, required, provided, name, value) -> None: ...
    def registered(self, required, provided, name: str = ''): ...
    def allRegistrations(self) -> Generator[Incomplete, Incomplete, None]: ...
    def unregister(self, required, provided, name, value: Incomplete | None = None): ...
    def subscribe(self, required, provided, value) -> None: ...
    def subscribed(self, required, provided, subscriber): ...
    def allSubscriptions(self) -> Generator[Incomplete, None, None]: ...
    def unsubscribe(self, required, provided, value: Incomplete | None = None) -> None: ...
    def rebuild(self): ...
    def get(self, _): ...

class LookupBase:
    def __init__(self) -> None: ...
    def changed(self, ignored: Incomplete | None = None) -> None: ...
    def lookup(self, required, provided, name: str = '', default: Incomplete | None = None): ...
    def lookup1(self, required, provided, name: str = '', default: Incomplete | None = None): ...
    def queryAdapter(self, object, provided, name: str = '', default: Incomplete | None = None): ...
    def adapter_hook(self, provided, object, name: str = '', default: Incomplete | None = None): ...
    def lookupAll(self, required, provided): ...
    def subscriptions(self, required, provided): ...

class VerifyingBase(LookupBaseFallback):
    def changed(self, originally_changed) -> None: ...
    def lookupAll(self, required, provided): ...
    def subscriptions(self, required, provided): ...

class AdapterLookupBase:
    def __init__(self, registry) -> None: ...
    def changed(self, ignored: Incomplete | None = None) -> None: ...
    def init_extendors(self) -> None: ...
    def add_extendor(self, provided) -> None: ...
    def remove_extendor(self, provided) -> None: ...
    def queryMultiAdapter(self, objects, provided, name: str = '', default: Incomplete | None = None): ...
    def names(self, required, provided): ...
    def subscribers(self, objects, provided): ...

class AdapterLookup(AdapterLookupBase, LookupBase): ...

class AdapterRegistry(BaseAdapterRegistry):
    LookupClass = AdapterLookup
    def __init__(self, bases=()) -> None: ...
    def changed(self, originally_changed) -> None: ...

class VerifyingAdapterLookup(AdapterLookupBase, VerifyingBase): ...

class VerifyingAdapterRegistry(BaseAdapterRegistry):
    LookupClass = VerifyingAdapterLookup
