from _typeshed import Incomplete

class NotFound(Exception): ...

class WSGITestApplication:
    request_log: Incomplete
    def __init__(self) -> None: ...
    def __call__(self, environ, start_response): ...

def handle_notfound(req) -> None: ...

class ParamsWrapper:
    params: Incomplete
    def __init__(self, params) -> None: ...
    def __getitem__(self, key): ...

def handle_resource(req, extra: Incomplete | None = None): ...
def forms(req): ...
def get_cookie(req): ...
def set_cookie(req): ...
def set_header(req): ...
def echo(req): ...
def redirect(req): ...
def echo_one(req): ...
def set_status(req): ...
