from _typeshed import Incomplete

__all__ = ['Response']

class Response:
    default_content_type: str
    default_charset: str
    unicode_errors: str
    default_conditional_response: bool
    default_body_encoding: str
    request: Incomplete
    environ: Incomplete
    status: Incomplete
    conditional_response: Incomplete
    def __init__(self, body: Incomplete | None = None, status: Incomplete | None = None, headerlist: Incomplete | None = None, app_iter: Incomplete | None = None, content_type: Incomplete | None = None, conditional_response: Incomplete | None = None, charset=..., **kw) -> None: ...
    @classmethod
    def from_file(cls, fp): ...
    def copy(self): ...
    status_code: Incomplete
    status_int: Incomplete
    headerlist: Incomplete
    headers: Incomplete
    body: Incomplete
    json: Incomplete
    json_body: Incomplete
    has_body: Incomplete
    text: Incomplete
    unicode_body: Incomplete
    ubody: Incomplete
    body_file: Incomplete
    content_length: Incomplete
    def write(self, text) -> None: ...
    app_iter: Incomplete
    allow: Incomplete
    vary: Incomplete
    content_encoding: Incomplete
    content_language: Incomplete
    content_location: Incomplete
    content_md5: Incomplete
    content_disposition: Incomplete
    accept_ranges: Incomplete
    content_range: Incomplete
    date: Incomplete
    expires: Incomplete
    last_modified: Incomplete
    etag: Incomplete
    @property
    def etag_strong(self): ...
    location: Incomplete
    pragma: Incomplete
    age: Incomplete
    retry_after: Incomplete
    server: Incomplete
    www_authenticate: Incomplete
    charset: Incomplete
    content_type: Incomplete
    content_type_params: Incomplete
    def set_cookie(self, name, value: str = '', max_age: Incomplete | None = None, path: str = '/', domain: Incomplete | None = None, secure: bool = False, httponly: bool = False, comment: Incomplete | None = None, expires: Incomplete | None = None, overwrite: bool = False, samesite: Incomplete | None = None) -> None: ...
    def delete_cookie(self, name, path: str = '/', domain: Incomplete | None = None) -> None: ...
    def unset_cookie(self, name, strict: bool = True) -> None: ...
    def merge_cookies(self, resp): ...
    cache_control: Incomplete
    cache_expires: Incomplete
    def encode_content(self, encoding: str = 'gzip', lazy: bool = False) -> None: ...
    def decode_content(self) -> None: ...
    def md5_etag(self, body: Incomplete | None = None, set_content_md5: bool = False) -> None: ...
    def __call__(self, environ, start_response): ...
    def conditional_response_app(self, environ, start_response): ...
    def app_iter_range(self, start, stop): ...

class ResponseBodyFile:
    mode: str
    closed: bool
    response: Incomplete
    write: Incomplete
    def __init__(self, response) -> None: ...
    encoding: Incomplete
    def writelines(self, seq) -> None: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def tell(self): ...

class AppIterRange:
    app_iter: Incomplete
    start: Incomplete
    stop: Incomplete
    def __init__(self, app_iter, start, stop) -> None: ...
    def __iter__(self): ...
    def next(self): ...
    __next__ = next
    def close(self) -> None: ...

class EmptyResponse:
    close: Incomplete
    def __init__(self, app_iter: Incomplete | None = None) -> None: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def next(self) -> None: ...
    __next__ = next
