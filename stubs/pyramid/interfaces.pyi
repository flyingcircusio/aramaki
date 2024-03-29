from _typeshed import Incomplete
from zope.interface import Interface

class IContextFound(Interface):
    request: Incomplete
IAfterTraversal = IContextFound

class IBeforeTraversal(Interface):
    request: Incomplete

class INewRequest(Interface):
    request: Incomplete

class INewResponse(Interface):
    request: Incomplete
    response: Incomplete

class IApplicationCreated(Interface):
    app: Incomplete
IWSGIApplicationCreatedEvent = IApplicationCreated

class IResponse(Interface):
    RequestClass: Incomplete
    def __call__(environ, start_response) -> None: ...
    accept_ranges: Incomplete
    age: Incomplete
    allow: Incomplete
    app_iter: Incomplete
    def app_iter_range(start, stop) -> None: ...
    identity: Incomplete
    authenticated_userid: Incomplete
    body: Incomplete
    body_file: Incomplete
    cache_control: Incomplete
    cache_expires: Incomplete
    charset: Incomplete
    def conditional_response_app(environ, start_response) -> None: ...
    content_disposition: Incomplete
    content_encoding: Incomplete
    content_language: Incomplete
    content_length: Incomplete
    content_location: Incomplete
    content_md5: Incomplete
    content_range: Incomplete
    content_type: Incomplete
    content_type_params: Incomplete
    def copy() -> None: ...
    date: Incomplete
    def delete_cookie(name, path: str = '/', domain: Incomplete | None = None) -> None: ...
    def encode_content(encoding: str = 'gzip', lazy: bool = False) -> None: ...
    environ: Incomplete
    etag: Incomplete
    expires: Incomplete
    headerlist: Incomplete
    headers: Incomplete
    is_authenticated: Incomplete
    last_modified: Incomplete
    location: Incomplete
    def md5_etag(body: Incomplete | None = None, set_content_md5: bool = False) -> None: ...
    def merge_cookies(resp) -> None: ...
    pragma: Incomplete
    request: Incomplete
    retry_after: Incomplete
    server: Incomplete
    def set_cookie(name, value: str = '', max_age: Incomplete | None = None, path: str = '/', domain: Incomplete | None = None, secure: bool = False, httponly: bool = False, comment: Incomplete | None = None, expires: Incomplete | None = None, overwrite: bool = False) -> None: ...
    status: Incomplete
    status_int: Incomplete
    unicode_body: Incomplete
    def unset_cookie(name, strict: bool = True) -> None: ...
    vary: Incomplete
    www_authenticate: Incomplete

class IException(Interface): ...

class IExceptionResponse(IException, IResponse):
    def prepare(environ) -> None: ...

class IDict(Interface):
    def __contains__(k) -> bool: ...
    def __setitem__(k, value) -> None: ...
    def __delitem__(k) -> None: ...
    def __getitem__(k) -> None: ...
    def __iter__(): ...
    def get(k, default: Incomplete | None = None) -> None: ...
    def items() -> None: ...
    def keys() -> None: ...
    def values() -> None: ...
    def pop(k, default: Incomplete | None = None) -> None: ...
    def popitem() -> None: ...
    def setdefault(k, default: Incomplete | None = None) -> None: ...
    def update(d) -> None: ...
    def clear() -> None: ...

class IBeforeRender(IDict):
    rendering_val: Incomplete

class IRendererInfo(Interface):
    name: Incomplete
    package: Incomplete
    type: Incomplete
    registry: Incomplete
    settings: Incomplete
    def clone() -> None: ...

class IRendererFactory(Interface):
    def __call__(info) -> None: ...

class IRenderer(Interface):
    def __call__(value, system) -> None: ...

class IViewMapper(Interface):
    def __call__(self, object) -> None: ...

class IViewMapperFactory(Interface):
    def __call__(self, **kw) -> None: ...

class ISecurityPolicy(Interface):
    def identity(request) -> None: ...
    def authenticated_userid(request) -> None: ...
    def permits(request, context, permission) -> None: ...
    def remember(request, userid, **kw) -> None: ...
    def forget(request, **kw) -> None: ...

class IAuthenticationPolicy(Interface):
    def authenticated_userid(request) -> None: ...
    def unauthenticated_userid(request) -> None: ...
    def effective_principals(request) -> None: ...
    def remember(request, userid, **kw) -> None: ...
    def forget(request) -> None: ...

class IAuthorizationPolicy(Interface):
    def permits(context, principals, permission) -> None: ...
    def principals_allowed_by_permission(context, permission) -> None: ...

class IMultiDict(IDict):
    def add(key, value) -> None: ...
    def dict_of_lists() -> None: ...
    def extend(other: Incomplete | None = None, **kwargs) -> None: ...
    def getall(key) -> None: ...
    def getone(key) -> None: ...
    def mixed() -> None: ...

class IRequest(Interface): ...
class ITweens(Interface): ...

class IRequestHandler(Interface):
    def __call__(self, request) -> None: ...

class IRequestExtensions(Interface):
    descriptors: Incomplete
    methods: Incomplete

class IRouteRequest(Interface): ...
class IAcceptOrder(Interface): ...

class IStaticURLInfo(Interface):
    def add(config, name, spec, **extra) -> None: ...
    def generate(path, request, **kw) -> None: ...
    def add_cache_buster(config, spec, cache_buster) -> None: ...

class IResponseFactory(Interface):
    def __call__(request) -> None: ...

class IRequestFactory(Interface):
    def __call__(environ) -> None: ...
    def blank(path) -> None: ...

class IViewClassifier(Interface): ...
class IExceptionViewClassifier(Interface): ...

class IView(Interface):
    def __call__(context, request) -> None: ...

class ISecuredView(IView):
    def __call_permissive__(context, request) -> None: ...
    def __permitted__(context, request) -> None: ...

class IMultiView(ISecuredView):
    def add(view, predicates, order, accept: Incomplete | None = None, phash: Incomplete | None = None) -> None: ...

class IRootFactory(Interface):
    def __call__(request) -> None: ...

class IDefaultRootFactory(Interface):
    def __call__(request) -> None: ...

class ITraverser(Interface):
    def __call__(request) -> None: ...
ITraverserFactory = ITraverser

class IViewPermission(Interface):
    def __call__(context, request) -> None: ...

class IRouter(Interface):
    registry: Incomplete
    def request_context(environ) -> None: ...
    def invoke_request(request) -> None: ...

class IExecutionPolicy(Interface):
    def __call__(environ, router) -> None: ...

class ISettings(IDict): ...

class ILocation(Interface):
    __parent__: Incomplete

class IDebugLogger(Interface): ...
ILogger = IDebugLogger

class IRoutePregenerator(Interface):
    def __call__(request, elements, kw) -> None: ...

class IRoute(Interface):
    name: Incomplete
    pattern: Incomplete
    factory: Incomplete
    predicates: Incomplete
    pregenerator: Incomplete
    def match(path) -> None: ...
    def generate(kw) -> None: ...

class IRoutesMapper(Interface):
    def get_routes() -> None: ...
    def has_routes() -> None: ...
    def get_route(name) -> None: ...
    def connect(name, pattern, factory: Incomplete | None = None, predicates=(), pregenerator: Incomplete | None = None, static: bool = True) -> None: ...
    def generate(name, kw) -> None: ...
    def __call__(request) -> None: ...

class IResourceURL(Interface):
    virtual_path: Incomplete
    physical_path: Incomplete
    virtual_path_tuple: Incomplete
    physical_path_tuple: Incomplete

class IPEP302Loader(Interface):
    def get_data(path) -> None: ...
    def is_package(fullname) -> None: ...
    def get_code(fullname) -> None: ...
    def get_source(fullname) -> None: ...
    def get_filename(fullname) -> None: ...

class IPackageOverrides(IPEP302Loader): ...

VH_ROOT_KEY: str

class ILocalizer(Interface): ...

class ILocaleNegotiator(Interface):
    def __call__(request) -> None: ...

class ITranslationDirectories(Interface): ...
class IDefaultPermission(Interface): ...

class IDefaultCSRFOptions(Interface):
    require_csrf: Incomplete
    token: Incomplete
    header: Incomplete
    safe_methods: Incomplete
    callback: Incomplete
    allow_no_origin: Incomplete

class ISessionFactory(Interface):
    def __call__(request) -> None: ...

class ISession(IDict):
    created: Incomplete
    new: Incomplete
    def invalidate() -> None: ...
    def changed() -> None: ...
    def flash(msg, queue: str = '', allow_duplicate: bool = True) -> None: ...
    def pop_flash(queue: str = '') -> None: ...
    def peek_flash(queue: str = '') -> None: ...

class ICSRFStoragePolicy(Interface):
    def new_csrf_token(request) -> None: ...
    def get_csrf_token(request) -> None: ...
    def check_csrf_token(request, token) -> None: ...

class IIntrospector(Interface):
    def get(category_name, discriminator, default: Incomplete | None = None) -> None: ...
    def get_category(category_name, default: Incomplete | None = None, sort_key: Incomplete | None = None) -> None: ...
    def categories() -> None: ...
    def categorized(sort_key: Incomplete | None = None) -> None: ...
    def remove(category_name, discriminator) -> None: ...
    def related(intr) -> None: ...
    def add(intr) -> None: ...
    def relate(*pairs) -> None: ...
    def unrelate(*pairs) -> None: ...

class IIntrospectable(Interface):
    title: Incomplete
    type_name: Incomplete
    order: Incomplete
    category_name: Incomplete
    discriminator: Incomplete
    discriminator_hash: Incomplete
    action_info: Incomplete
    def relate(category_name, discriminator) -> None: ...
    def unrelate(category_name, discriminator) -> None: ...
    def register(introspector, action_info) -> None: ...
    def __hash__(): ...

class IActionInfo(Interface):
    file: Incomplete
    line: Incomplete

class IAssetDescriptor(Interface):
    def absspec() -> None: ...
    def abspath() -> None: ...
    def stream() -> None: ...
    def isdir() -> None: ...
    def listdir() -> None: ...
    def exists() -> None: ...

class IJSONAdapter(Interface): ...
class IPredicateList(Interface): ...

class IPredicateInfo(Interface):
    package: Incomplete
    registry: Incomplete
    settings: Incomplete
    def maybe_dotted(value) -> None: ...

class IPredicateFactory(Interface):
    def __call__(value, info) -> None: ...

class IPredicate(Interface):
    def text() -> None: ...
    def phash() -> None: ...

class IRoutePredicate(IPredicate):
    def __call__(info, request) -> None: ...

class ISubscriberPredicate(IPredicate):
    def __call__(*args) -> None: ...

class IViewPredicate(IPredicate):
    def __call__(context, request) -> None: ...

class IViewDeriver(Interface):
    options: Incomplete
    def __call__(view, info) -> None: ...

class IViewDeriverInfo(Interface):
    registry: Incomplete
    package: Incomplete
    settings: Incomplete
    options: Incomplete
    predicates: Incomplete
    original_view: Incomplete
    exception_only: Incomplete

class IViewDerivers(Interface): ...

class ICacheBuster(Interface):
    def __call__(request, subpath, kw) -> None: ...

PHASE0_CONFIG: int
PHASE1_CONFIG: int
PHASE2_CONFIG: int
PHASE3_CONFIG: int
