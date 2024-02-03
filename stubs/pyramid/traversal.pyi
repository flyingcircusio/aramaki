from _typeshed import Incomplete
from pyramid.encode import url_quote as url_quote
from pyramid.exceptions import URLDecodeError as URLDecodeError
from pyramid.interfaces import IRequestFactory as IRequestFactory, IResourceURL as IResourceURL, ITraverser as ITraverser, VH_ROOT_KEY as VH_ROOT_KEY
from pyramid.location import lineage as lineage
from pyramid.threadlocal import get_current_registry as get_current_registry
from pyramid.util import ascii_ as ascii_, is_nonstr_iter as is_nonstr_iter, text_ as text_

PATH_SEGMENT_SAFE: str
PATH_SAFE: Incomplete

def find_root(resource): ...
def find_resource(resource, path): ...
find_model = find_resource

def find_interface(resource, class_or_interface): ...
def resource_path(resource, *elements): ...
model_path = resource_path

def traverse(resource, path): ...
def resource_path_tuple(resource, *elements): ...
model_path_tuple = resource_path_tuple

def virtual_root(resource, request): ...
def traversal_path(path): ...
def traversal_path_info(path): ...
def split_path_info(path): ...
def decode_path_info(path): ...
def unquote_bytes_to_wsgi(bytestring): ...
def quote_path_segment(segment, safe=...): ...

class ResourceTreeTraverser:
    VH_ROOT_KEY = VH_ROOT_KEY
    VIEW_SELECTOR: str
    root: Incomplete
    def __init__(self, root) -> None: ...
    def __call__(self, request): ...
ModelGraphTraverser = ResourceTreeTraverser

class ResourceURL:
    VH_ROOT_KEY = VH_ROOT_KEY
    virtual_path: Incomplete
    physical_path: Incomplete
    virtual_path_tuple: Incomplete
    physical_path_tuple: Incomplete
    def __init__(self, resource, request) -> None: ...

class DefaultRootFactory:
    __parent__: Incomplete
    def __init__(self, request) -> None: ...