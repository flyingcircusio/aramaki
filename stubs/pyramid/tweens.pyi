from pyramid.httpexceptions import HTTPNotFound as HTTPNotFound
from pyramid.util import reraise as reraise

def excview_tween_factory(handler, registry): ...

MAIN: str
INGRESS: str
EXCVIEW: str
