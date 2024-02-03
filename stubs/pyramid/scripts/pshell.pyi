import pkg_resources
from _typeshed import Incomplete
from collections.abc import Generator
from pyramid.paster import bootstrap as bootstrap
from pyramid.scripts.common import get_config_loader as get_config_loader, parse_vars as parse_vars
from pyramid.settings import aslist as aslist
from pyramid.util import DottedNameResolver as DottedNameResolver, make_contextmanager as make_contextmanager

def main(argv=..., quiet: bool = False): ...
def python_shell_runner(env, help, interact=...) -> None: ...

class PShellCommand:
    description: str
    bootstrap: Incomplete
    get_config_loader: Incomplete
    pkg_resources = pkg_resources
    parser: Incomplete
    default_runner = python_shell_runner
    loaded_objects: Incomplete
    object_help: Incomplete
    preferred_shells: Incomplete
    setup: Incomplete
    pystartup: Incomplete
    resolver: Incomplete
    quiet: Incomplete
    args: Incomplete
    def __init__(self, argv, quiet: bool = False) -> None: ...
    def pshell_file_config(self, loader, defaults) -> None: ...
    def out(self, msg) -> None: ...
    env: Incomplete
    closer: Incomplete
    def run(self, shell: Incomplete | None = None): ...
    help: Incomplete
    def setup_env(self) -> Generator[None, None, None]: ...
    def show_shells(self): ...
    def find_all_shells(self): ...
    def make_shell(self): ...
