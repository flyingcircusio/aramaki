from _typeshed import Incomplete
from pyramid.interfaces import ITweens as ITweens
from pyramid.paster import bootstrap as bootstrap, setup_logging as setup_logging
from pyramid.scripts.common import parse_vars as parse_vars
from pyramid.tweens import INGRESS as INGRESS, MAIN as MAIN

def main(argv=..., quiet: bool = False): ...

class PTweensCommand:
    description: str
    parser: Incomplete
    stdout: Incomplete
    bootstrap: Incomplete
    setup_logging: Incomplete
    quiet: Incomplete
    args: Incomplete
    def __init__(self, argv, quiet: bool = False) -> None: ...
    def out(self, msg) -> None: ...
    def show_chain(self, chain) -> None: ...
    def run(self): ...
