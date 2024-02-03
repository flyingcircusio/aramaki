from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple

OWS_re: str
tchar_re: str
token_re: Incomplete
token_compiled_re: Incomplete
qvalue_re: str
weight_re: Incomplete

class AcceptOffer(NamedTuple('AcceptOffer', [('type', Incomplete), ('subtype', Incomplete), ('params', Incomplete)])): ...

class Accept:
    vchar_re: str
    obs_text_re: str
    qdtext_re: Incomplete
    quoted_pair_re: Incomplete
    quoted_string_re: Incomplete
    type_re = token_re
    subtype_re = token_re
    parameter_re: Incomplete
    media_range_re: Incomplete
    accept_ext_re: Incomplete
    accept_params_re: Incomplete
    media_range_n_accept_params_re: Incomplete
    media_range_n_accept_params_compiled_re: Incomplete
    accept_compiled_re: Incomplete
    parameters_compiled_re: Incomplete
    accept_ext_compiled_re: Incomplete
    media_type_re = media_range_re
    media_type_compiled_re: Incomplete
    @classmethod
    def parse(cls, value): ...
    @classmethod
    def parse_offer(cls, offer): ...

class AcceptValidHeader(Accept):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def __radd__(self, other): ...
    def accept_html(self): ...
    accepts_html: Incomplete
    def acceptable_offers(self, offers): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def quality(self, offer): ...

class MIMEAccept(Accept):
    def __init__(self, header_value) -> None: ...
    @staticmethod
    def parse(value) -> Generator[Incomplete, None, None]: ...
    def __iter__(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...
    def __contains__(self, offer) -> bool: ...
    def quality(self, offer): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def accept_html(self): ...

class _AcceptInvalidOrNoHeader(Accept):
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def accept_html(self): ...
    accepts_html: Incomplete
    def acceptable_offers(self, offers): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def quality(self, offer): ...

class AcceptNoHeader(_AcceptInvalidOrNoHeader):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

class AcceptInvalidHeader(_AcceptInvalidOrNoHeader):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

def create_accept_header(header_value): ...
def accept_property(): ...

class AcceptCharset:
    charset_re = token_re
    charset_n_weight_re: Incomplete
    charset_n_weight_compiled_re: Incomplete
    accept_charset_compiled_re: Incomplete
    @classmethod
    def parse(cls, value): ...

class AcceptCharsetValidHeader(AcceptCharset):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def __radd__(self, other): ...
    def acceptable_offers(self, offers): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def quality(self, offer): ...

class _AcceptCharsetInvalidOrNoHeader(AcceptCharset):
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def acceptable_offers(self, offers): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def quality(self, offer): ...

class AcceptCharsetNoHeader(_AcceptCharsetInvalidOrNoHeader):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

class AcceptCharsetInvalidHeader(_AcceptCharsetInvalidOrNoHeader):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

def create_accept_charset_header(header_value): ...
def accept_charset_property(): ...

class AcceptEncoding:
    codings_re = token_re
    codings_n_weight_re: Incomplete
    codings_n_weight_compiled_re: Incomplete
    accept_encoding_compiled_re: Incomplete
    @classmethod
    def parse(cls, value): ...

class AcceptEncodingValidHeader(AcceptEncoding):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def __radd__(self, other): ...
    def acceptable_offers(self, offers): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def quality(self, offer): ...

class _AcceptEncodingInvalidOrNoHeader(AcceptEncoding):
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def acceptable_offers(self, offers): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def quality(self, offer): ...

class AcceptEncodingNoHeader(_AcceptEncodingInvalidOrNoHeader):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

class AcceptEncodingInvalidHeader(_AcceptEncodingInvalidOrNoHeader):
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

def create_accept_encoding_header(header_value): ...
def accept_encoding_property(): ...

class AcceptLanguage:
    lang_range_re: str
    lang_range_n_weight_re: Incomplete
    lang_range_n_weight_compiled_re: Incomplete
    accept_language_compiled_re: Incomplete
    @classmethod
    def parse(cls, value): ...

class AcceptLanguageValidHeader(AcceptLanguage):
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __add__(self, other): ...
    def __nonzero__(self): ...
    __bool__ = __nonzero__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def __radd__(self, other): ...
    def basic_filtering(self, language_tags): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def lookup(self, language_tags, default_range: Incomplete | None = None, default_tag: Incomplete | None = None, default: Incomplete | None = None): ...
    def quality(self, offer): ...

class _AcceptLanguageInvalidOrNoHeader(AcceptLanguage):
    def __nonzero__(self): ...
    __bool__ = __nonzero__
    def __contains__(self, offer) -> bool: ...
    def __iter__(self): ...
    def basic_filtering(self, language_tags): ...
    def best_match(self, offers, default_match: Incomplete | None = None): ...
    def lookup(self, language_tags: Incomplete | None = None, default_range: Incomplete | None = None, default_tag: Incomplete | None = None, default: Incomplete | None = None): ...
    def quality(self, offer): ...

class AcceptLanguageNoHeader(_AcceptLanguageInvalidOrNoHeader):
    def __init__(self) -> None: ...
    def copy(self): ...
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

class AcceptLanguageInvalidHeader(_AcceptLanguageInvalidOrNoHeader):
    def __init__(self, header_value) -> None: ...
    def copy(self): ...
    @property
    def header_value(self): ...
    @property
    def parsed(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...

def create_accept_language_header(header_value): ...
def accept_language_property(): ...
