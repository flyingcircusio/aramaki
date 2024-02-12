from _typeshed import Incomplete

__all__ = ['DebugApp', 'make_debug_app']

class DebugApp:
    form: Incomplete
    show_form: Incomplete
    def __init__(self, form: Incomplete | None = None, show_form: bool = False) -> None: ...
    def __call__(self, environ, start_response): ...

def make_debug_app(global_conf, **local_conf): ...
