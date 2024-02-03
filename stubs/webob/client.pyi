from _typeshed import Incomplete

__all__ = ['send_request_app', 'SendRequest']

class SendRequest:
    HTTPConnection: Incomplete
    HTTPSConnection: Incomplete
    def __init__(self, HTTPConnection=..., HTTPSConnection=...) -> None: ...
    def __call__(self, environ, start_response): ...
    filtered_headers: Incomplete
    MULTILINE_RE: Incomplete
    def parse_headers(self, message): ...

send_request_app: Incomplete
