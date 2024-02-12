import zope.testbrowser.browser
from _typeshed import Incomplete
from collections.abc import Generator
from zope.testbrowser.browser import HostNotAllowed as HostNotAllowed

class Browser(zope.testbrowser.browser.Browser):
    def __init__(self, url: Incomplete | None = None, wsgi_app: Incomplete | None = None) -> None: ...

basicre: Incomplete

def auth_header(header): ...
def is_wanted_header(header): ...

class AuthorizationMiddleware:
    wsgi_stack: Incomplete
    def __init__(self, wsgi_stack) -> None: ...
    def __call__(self, environ, start_response) -> Generator[Incomplete, Incomplete, None]: ...

class Layer:
    __bases__: Incomplete
    @classmethod
    def get_app(cls): ...
    def make_wsgi_app(self) -> None: ...
    def cooperative_super(self, method_name) -> None: ...
    def setUp(self) -> None: ...
    def tearDown(self) -> None: ...

class TestBrowserLayer:
    def cooperative_super(self, method_name): ...
    def make_wsgi_app(self): ...
    def testSetUp(self) -> None: ...
    def testTearDown(self) -> None: ...
