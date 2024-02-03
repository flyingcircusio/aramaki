import io
from _typeshed import Incomplete

__all__ = ["BaseRequest", "Request", "LegacyRequest"]

class _NoDefault: ...

class BaseRequest:
    request_body_tempfile_limit: Incomplete
    method: Incomplete
    def __init__(
        self,
        environ,
        charset: Incomplete | None = None,
        unicode_errors: Incomplete | None = None,
        decode_param_names: Incomplete | None = None,
        **kw
    ) -> None: ...
    def encget(self, key, default=..., encattr: Incomplete | None = None): ...
    def encset(self, key, val, encattr: Incomplete | None = None) -> None: ...
    @property
    def charset(self): ...
    @charset.setter
    def charset(self, charset) -> None: ...
    def decode(
        self, charset: Incomplete | None = None, errors: str = "strict"
    ): ...
    @property
    def body_file(self): ...
    content_length: Incomplete
    body_file_raw: Incomplete
    is_body_seekable: bool
    @body_file.setter
    def body_file(self, value) -> None: ...
    @property
    def body_file_seekable(self): ...
    url_encoding: Incomplete
    scheme: Incomplete
    http_version: Incomplete
    remote_user: Incomplete
    remote_host: Incomplete
    remote_addr: Incomplete
    query_string: Incomplete
    server_name: Incomplete
    server_port: Incomplete
    script_name: Incomplete
    path_info: Incomplete
    uscript_name = script_name
    upath_info = path_info
    content_type: Incomplete
    headers: Incomplete
    @property
    def client_addr(self): ...
    @property
    def host_port(self): ...
    @property
    def host_url(self): ...
    @property
    def application_url(self): ...
    @property
    def path_url(self): ...
    @property
    def path(self): ...
    @property
    def path_qs(self): ...
    @property
    def url(self): ...
    def relative_url(self, other_url, to_application: bool = False): ...
    def path_info_pop(self, pattern: Incomplete | None = None): ...
    def path_info_peek(self): ...
    urlvars: Incomplete
    urlargs: Incomplete
    @property
    def is_xhr(self): ...
    host: Incomplete
    @property
    def domain(self): ...
    @property
    def body(self): ...
    @body.setter
    def body(self, value) -> None: ...
    def body(self) -> None: ...
    json: Incomplete
    json_body: Incomplete
    text: Incomplete
    @property
    def POST(self): ...
    @property
    def GET(self): ...
    @property
    def params(self): ...
    @property
    def cookies(self): ...
    @cookies.setter
    def cookies(self, val) -> None: ...
    def copy(self): ...
    def copy_get(self): ...
    @property
    def is_body_readable(self): ...
    @is_body_readable.setter
    def is_body_readable(self, flag) -> None: ...
    def make_body_seekable(self) -> None: ...
    def copy_body(self) -> None: ...
    def make_tempfile(self): ...
    def remove_conditional_headers(
        self,
        remove_encoding: bool = True,
        remove_range: bool = True,
        remove_match: bool = True,
        remove_modified: bool = True,
    ) -> None: ...
    accept: Incomplete
    accept_charset: Incomplete
    accept_encoding: Incomplete
    accept_language: Incomplete
    authorization: Incomplete
    cache_control: Incomplete
    if_match: Incomplete
    if_none_match: Incomplete
    date: Incomplete
    if_modified_since: Incomplete
    if_unmodified_since: Incomplete
    if_range: Incomplete
    max_forwards: Incomplete
    pragma: Incomplete
    range: Incomplete
    referer: Incomplete
    referrer = referer
    user_agent: Incomplete
    def as_bytes(self, skip_body: bool = False): ...
    def as_text(self): ...
    @classmethod
    def from_bytes(cls, b): ...
    @classmethod
    def from_text(cls, s): ...
    @classmethod
    def from_file(cls, fp): ...
    def call_application(self, application, catch_exc_info: bool = False): ...
    ResponseClass: Incomplete
    def send(
        self,
        application: Incomplete | None = None,
        catch_exc_info: bool = False,
    ): ...
    get_response = send
    def make_default_send_app(self): ...
    @classmethod
    def blank(
        cls,
        path,
        environ: Incomplete | None = None,
        base_url: Incomplete | None = None,
        headers: Incomplete | None = None,
        POST: Incomplete | None = None,
        **kw
    ): ...

class LegacyRequest(BaseRequest):
    uscript_name: Incomplete
    upath_info: Incomplete
    def encget(self, key, default=..., encattr: Incomplete | None = None): ...

class AdhocAttrMixin:
    def __setattr__(self, attr, value, DEFAULT=...) -> None: ...
    def __getattr__(self, attr, DEFAULT=...): ...
    def __delattr__(self, attr, DEFAULT=...): ...

class Request(AdhocAttrMixin, BaseRequest): ...
class DisconnectionError(IOError): ...

class LimitedLengthFile(io.RawIOBase):
    file: Incomplete
    maxlen: Incomplete
    remaining: Incomplete
    def __init__(self, file, maxlen) -> None: ...
    def fileno(self): ...
    @staticmethod
    def readable(): ...
    def readinto(self, buff): ...

class FakeCGIBody(io.RawIOBase):
    vars: Incomplete
    content_type: Incomplete
    file: Incomplete
    def __init__(self, vars, content_type) -> None: ...
    def fileno(self) -> None: ...
    @staticmethod
    def readable(): ...
    def readinto(self, buff): ...

class Transcoder:
    charset: Incomplete
    errors: Incomplete
    def __init__(self, charset, errors: str = "strict") -> None: ...
    def transcode_query(self, q): ...
    def transcode_fs(self, fs, content_type): ...
