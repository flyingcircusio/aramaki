from _typeshed import Incomplete
from webob.response import Response

__all__ = ['HTTPExceptionMiddleware', 'status_map', 'HTTPException', 'WSGIHTTPException', 'HTTPError', 'HTTPRedirection', 'HTTPOk', 'HTTPCreated', 'HTTPAccepted', 'HTTPNonAuthoritativeInformation', 'HTTPNoContent', 'HTTPResetContent', 'HTTPPartialContent', 'HTTPMultipleChoices', 'HTTPMovedPermanently', 'HTTPFound', 'HTTPSeeOther', 'HTTPNotModified', 'HTTPUseProxy', 'HTTPTemporaryRedirect', 'HTTPPermanentRedirect', 'HTTPClientError', 'HTTPBadRequest', 'HTTPUnauthorized', 'HTTPPaymentRequired', 'HTTPForbidden', 'HTTPNotFound', 'HTTPMethodNotAllowed', 'HTTPNotAcceptable', 'HTTPProxyAuthenticationRequired', 'HTTPRequestTimeout', 'HTTPConflict', 'HTTPGone', 'HTTPLengthRequired', 'HTTPPreconditionFailed', 'HTTPRequestEntityTooLarge', 'HTTPRequestURITooLong', 'HTTPUnsupportedMediaType', 'HTTPRequestRangeNotSatisfiable', 'HTTPExpectationFailed', 'HTTPUnprocessableEntity', 'HTTPLocked', 'HTTPFailedDependency', 'HTTPPreconditionRequired', 'HTTPTooManyRequests', 'HTTPRequestHeaderFieldsTooLarge', 'HTTPUnavailableForLegalReasons', 'HTTPServerError', 'HTTPInternalServerError', 'HTTPNotImplemented', 'HTTPBadGateway', 'HTTPServiceUnavailable', 'HTTPGatewayTimeout', 'HTTPVersionNotSupported', 'HTTPInsufficientStorage', 'HTTPNetworkAuthenticationRequired']

class _lazified:
    func: Incomplete
    value: Incomplete
    def __init__(self, func, value) -> None: ...

class HTTPException(Exception):
    wsgi_response: Incomplete
    def __init__(self, message, wsgi_response) -> None: ...
    def __call__(self, environ, start_response): ...

class WSGIHTTPException(Response, HTTPException):
    code: int
    title: str
    explanation: str
    body_template_obj: Incomplete
    plain_template_obj: Incomplete
    html_template_obj: Incomplete
    empty_body: bool
    detail: Incomplete
    comment: Incomplete
    body_template: Incomplete
    def __init__(self, detail: Incomplete | None = None, headers: Incomplete | None = None, comment: Incomplete | None = None, body_template: Incomplete | None = None, json_formatter: Incomplete | None = None, **kw) -> None: ...
    def plain_body(self, environ): ...
    def html_body(self, environ): ...
    def json_formatter(self, body, status, title, environ): ...
    def json_body(self, environ): ...
    def generate_response(self, environ, start_response): ...
    def __call__(self, environ, start_response): ...
    @property
    def wsgi_response(self): ...

class HTTPError(WSGIHTTPException): ...
class HTTPRedirection(WSGIHTTPException): ...

class HTTPOk(WSGIHTTPException):
    code: int
    title: str

class HTTPCreated(HTTPOk):
    code: int
    title: str

class HTTPAccepted(HTTPOk):
    code: int
    title: str
    explanation: str

class HTTPNonAuthoritativeInformation(HTTPOk):
    code: int
    title: str

class HTTPNoContent(HTTPOk):
    code: int
    title: str
    empty_body: bool

class HTTPResetContent(HTTPOk):
    code: int
    title: str
    empty_body: bool

class HTTPPartialContent(HTTPOk):
    code: int
    title: str

class _HTTPMove(HTTPRedirection):
    explanation: str
    body_template_obj: Incomplete
    location: Incomplete
    add_slash: Incomplete
    def __init__(self, detail: Incomplete | None = None, headers: Incomplete | None = None, comment: Incomplete | None = None, body_template: Incomplete | None = None, location: Incomplete | None = None, add_slash: bool = False) -> None: ...
    def __call__(self, environ, start_response): ...

class HTTPMultipleChoices(_HTTPMove):
    code: int
    title: str

class HTTPMovedPermanently(_HTTPMove):
    code: int
    title: str

class HTTPFound(_HTTPMove):
    code: int
    title: str
    explanation: str

class HTTPSeeOther(_HTTPMove):
    code: int
    title: str

class HTTPNotModified(HTTPRedirection):
    code: int
    title: str
    empty_body: bool

class HTTPUseProxy(_HTTPMove):
    code: int
    title: str
    explanation: str

class HTTPTemporaryRedirect(_HTTPMove):
    code: int
    title: str

class HTTPPermanentRedirect(_HTTPMove):
    code: int
    title: str

class HTTPClientError(HTTPError):
    code: int
    title: str
    explanation: str

class HTTPBadRequest(HTTPClientError): ...

class HTTPUnauthorized(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPPaymentRequired(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPForbidden(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPNotFound(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPMethodNotAllowed(HTTPClientError):
    code: int
    title: str
    body_template_obj: Incomplete

class HTTPNotAcceptable(HTTPClientError):
    code: int
    title: str
    body_template_obj: Incomplete

class HTTPProxyAuthenticationRequired(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPRequestTimeout(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPConflict(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPGone(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPLengthRequired(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPPreconditionFailed(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPRequestEntityTooLarge(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPRequestURITooLong(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPUnsupportedMediaType(HTTPClientError):
    code: int
    title: str
    body_template_obj: Incomplete

class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPExpectationFailed(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPUnprocessableEntity(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPLocked(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPFailedDependency(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPPreconditionRequired(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPTooManyRequests(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPUnavailableForLegalReasons(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPServerError(HTTPError):
    code: int
    title: str
    explanation: str

class HTTPInternalServerError(HTTPServerError): ...

class HTTPNotImplemented(HTTPServerError):
    code: int
    title: str
    body_template_obj: Incomplete

class HTTPBadGateway(HTTPServerError):
    code: int
    title: str
    explanation: str

class HTTPServiceUnavailable(HTTPServerError):
    code: int
    title: str
    explanation: str

class HTTPGatewayTimeout(HTTPServerError):
    code: int
    title: str
    explanation: str

class HTTPVersionNotSupported(HTTPServerError):
    code: int
    title: str
    explanation: str

class HTTPInsufficientStorage(HTTPServerError):
    code: int
    title: str
    explanation: str

class HTTPNetworkAuthenticationRequired(HTTPServerError):
    code: int
    title: str
    explanation: str

class HTTPExceptionMiddleware:
    application: Incomplete
    def __init__(self, application) -> None: ...
    def __call__(self, environ, start_response): ...

status_map: Incomplete
