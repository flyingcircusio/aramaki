import venusian
from _typeshed import Incomplete
from pyramid.interfaces import IResponse as IResponse, IResponseFactory as IResponseFactory
from webob import Response as _Response

class Response(_Response): ...

class FileResponse(Response):
    last_modified: Incomplete
    app_iter: Incomplete
    content_length: Incomplete
    cache_expires: Incomplete
    def __init__(self, path, request: Incomplete | None = None, cache_max_age: Incomplete | None = None, content_type: Incomplete | None = None, content_encoding: Incomplete | None = None) -> None: ...

class FileIter:
    file: Incomplete
    block_size: Incomplete
    def __init__(self, file, block_size=...) -> None: ...
    def __iter__(self): ...
    def __next__(self): ...
    def close(self) -> None: ...

class response_adapter:
    venusian = venusian
    types_or_ifaces: Incomplete
    depth: Incomplete
    category: Incomplete
    kwargs: Incomplete
    def __init__(self, *types_or_ifaces, **kwargs) -> None: ...
    def register(self, scanner, name, wrapped) -> None: ...
    def __call__(self, wrapped): ...
