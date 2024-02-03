import venusian
from _typeshed import Incomplete
from pyramid.interfaces import IApplicationCreated as IApplicationCreated, IBeforeRender as IBeforeRender, IBeforeTraversal as IBeforeTraversal, IContextFound as IContextFound, INewRequest as INewRequest, INewResponse as INewResponse

class subscriber:
    venusian = venusian
    ifaces: Incomplete
    predicates: Incomplete
    depth: Incomplete
    category: Incomplete
    def __init__(self, *ifaces, **predicates) -> None: ...
    def register(self, scanner, name, wrapped) -> None: ...
    def __call__(self, wrapped): ...

class NewRequest:
    request: Incomplete
    def __init__(self, request) -> None: ...

class NewResponse:
    request: Incomplete
    response: Incomplete
    def __init__(self, request, response) -> None: ...

class BeforeTraversal:
    request: Incomplete
    def __init__(self, request) -> None: ...

class ContextFound:
    request: Incomplete
    def __init__(self, request) -> None: ...
AfterTraversal = ContextFound

class ApplicationCreated:
    app: Incomplete
    object: Incomplete
    def __init__(self, app) -> None: ...
WSGIApplicationCreatedEvent = ApplicationCreated

class BeforeRender(dict):
    rendering_val: Incomplete
    def __init__(self, system, rendering_val: Incomplete | None = None) -> None: ...
