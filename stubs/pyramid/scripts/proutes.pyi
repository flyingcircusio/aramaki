from _typeshed import Incomplete
from pyramid.config import not_ as not_
from pyramid.interfaces import IRouteRequest as IRouteRequest
from pyramid.paster import bootstrap as bootstrap
from pyramid.scripts.common import get_config_loader as get_config_loader, parse_vars as parse_vars
from pyramid.static import static_view as static_view

PAD: int
ANY_KEY: str
UNKNOWN_KEY: str

def main(argv=..., quiet: bool = False): ...
def get_route_data(route, registry): ...

class PRoutesCommand:
    description: str
    bootstrap: Incomplete
    get_config_loader: Incomplete
    stdout: Incomplete
    parser: Incomplete
    args: Incomplete
    quiet: Incomplete
    available_formats: Incomplete
    column_format: Incomplete
    def __init__(self, argv, quiet: bool = False) -> None: ...
    def validate_formats(self, formats): ...
    def proutes_file_config(self, loader, global_conf: Incomplete | None = None) -> None: ...
    def out(self, msg) -> None: ...
    def run(self, quiet: bool = False): ...
