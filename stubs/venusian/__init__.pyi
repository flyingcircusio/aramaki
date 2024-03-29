from _typeshed import Incomplete
from collections.abc import Generator
from venusian.advice import getFrameInfo as getFrameInfo
from venusian.compat import compat_find_loader as compat_find_loader

ATTACH_ATTR: str
LIFTONLY_ATTR: str

class Scanner:
    def __init__(self, **kw) -> None: ...
    def scan(self, package, categories: Incomplete | None = None, onerror: Incomplete | None = None, ignore: Incomplete | None = None): ...

class AttachInfo:
    def __init__(self, **kw) -> None: ...

class Categories(dict):
    attached_id: Incomplete
    lifted: bool
    def __init__(self, attached_to) -> None: ...
    def attached_to(self, mod_name, name, obj): ...

def attach(wrapped, callback, category: Incomplete | None = None, depth: int = 1, name: Incomplete | None = None): ...
def walk_packages(path: Incomplete | None = None, prefix: str = '', onerror: Incomplete | None = None, ignore: Incomplete | None = None) -> Generator[Incomplete, None, Incomplete]: ...

class lift:
    categories: Incomplete
    def __init__(self, categories: Incomplete | None = None) -> None: ...
    def __call__(self, wrapped): ...

class onlyliftedfrom:
    def __call__(self, wrapped): ...
