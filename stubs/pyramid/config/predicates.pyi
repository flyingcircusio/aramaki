from _typeshed import Incomplete
from pyramid.exceptions import ConfigurationError as ConfigurationError
from pyramid.interfaces import IPredicateList as IPredicateList, PHASE1_CONFIG as PHASE1_CONFIG
from pyramid.predicates import Notted as Notted
from pyramid.registry import predvalseq as predvalseq
from pyramid.util import TopologicalSorter as TopologicalSorter, bytes_ as bytes_, is_nonstr_iter as is_nonstr_iter

MAX_ORDER: Incomplete
DEFAULT_PHASH: Incomplete

class PredicateConfiguratorMixin:
    def get_predlist(self, name): ...

class not_:
    value: Incomplete
    def __init__(self, value) -> None: ...

class PredicateInfo:
    package: Incomplete
    registry: Incomplete
    settings: Incomplete
    maybe_dotted: Incomplete
    def __init__(self, package, registry, settings, maybe_dotted) -> None: ...

class PredicateList:
    sorter: Incomplete
    last_added: Incomplete
    def __init__(self) -> None: ...
    def add(self, name, factory, weighs_more_than: Incomplete | None = None, weighs_less_than: Incomplete | None = None) -> None: ...
    def names(self): ...
    def make(self, config, **kw): ...

def normalize_accept_offer(offer): ...
def sort_accept_offers(offers, order: Incomplete | None = None): ...
