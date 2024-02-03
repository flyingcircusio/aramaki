from _typeshed import Incomplete
from pyramid.request import Request as Request
from pyramid.scripts.common import get_config_loader as get_config_loader, parse_vars as parse_vars

def main(argv=..., quiet: bool = False): ...

class PRequestCommand:
    description: str
    parser: Incomplete
    stdin: Incomplete
    quiet: Incomplete
    args: Incomplete
    def __init__(self, argv, quiet: bool = False) -> None: ...
    def out(self, msg) -> None: ...
    def run(self): ...
