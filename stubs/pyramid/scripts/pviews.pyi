from _typeshed import Incomplete
from pyramid.interfaces import IMultiView as IMultiView
from pyramid.paster import bootstrap as bootstrap, setup_logging as setup_logging
from pyramid.request import Request as Request
from pyramid.scripts.common import parse_vars as parse_vars

def main(argv=..., quiet: bool = False): ...

class PViewsCommand:
    description: str
    stdout: Incomplete
    parser: Incomplete
    bootstrap: Incomplete
    setup_logging: Incomplete
    quiet: Incomplete
    args: Incomplete
    def __init__(self, argv, quiet: bool = False) -> None: ...
    def out(self, msg) -> None: ...
    def output_route_attrs(self, attrs, indent) -> None: ...
    def output_view_info(self, view_wrapper, level: int = 1) -> None: ...
    def run(self): ...
