from _typeshed import Incomplete
from pyramid.interfaces import IExceptionResponse as IExceptionResponse
from pyramid.response import Response as Response
from pyramid.util import text_ as text_

class HTTPException(Response, Exception):
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
    content_type: str
    charset: Incomplete
    excobj: Incomplete
    app_iter: Incomplete
    body: Incomplete
    def prepare(self, environ): ...
    @property
    def wsgi_response(self): ...
    exception = wsgi_response
    def __call__(self, environ, start_response): ...
WSGIHTTPException = HTTPException

class HTTPError(HTTPException): ...
class HTTPRedirection(HTTPException): ...
class HTTPSuccessful(HTTPException): ...

class HTTPOk(HTTPSuccessful):
    code: int
    title: str

class HTTPCreated(HTTPSuccessful):
    code: int
    title: str

class HTTPAccepted(HTTPSuccessful):
    code: int
    title: str
    explanation: str

class HTTPNonAuthoritativeInformation(HTTPSuccessful):
    code: int
    title: str

class HTTPNoContent(HTTPSuccessful):
    code: int
    title: str
    empty_body: bool

class HTTPResetContent(HTTPSuccessful):
    code: int
    title: str
    empty_body: bool

class HTTPPartialContent(HTTPSuccessful):
    code: int
    title: str

class _HTTPMove(HTTPRedirection):
    explanation: str
    body_template_obj: Incomplete
    def __init__(self, location: str = '', detail: Incomplete | None = None, headers: Incomplete | None = None, comment: Incomplete | None = None, body_template: Incomplete | None = None, **kw) -> None: ...

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

class HTTPBadRequest(HTTPClientError):
    explanation: str

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
    result: Incomplete
    def __init__(self, detail: Incomplete | None = None, headers: Incomplete | None = None, comment: Incomplete | None = None, body_template: Incomplete | None = None, result: Incomplete | None = None, **kw) -> None: ...

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

class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPExpectationFailed(HTTPClientError):
    code: int
    title: str
    explanation: str

class HTTPImATeapot(HTTPClientError):
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

class HTTPServerError(HTTPError):
    code: int
    title: str

class HTTPInternalServerError(HTTPServerError):
    explanation: str

class HTTPNotImplemented(HTTPServerError):
    code: int
    title: str

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

def exception_response(status_code, **kw): ...
def default_exceptionresponse_view(context, request): ...

status_map: Incomplete
code: Incomplete
