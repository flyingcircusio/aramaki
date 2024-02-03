from _typeshed import Incomplete
from pyramid.interfaces import IAuthenticationPolicy as IAuthenticationPolicy, IAuthorizationPolicy as IAuthorizationPolicy, ISecuredView as ISecuredView, ISecurityPolicy as ISecurityPolicy, IView as IView, IViewClassifier as IViewClassifier
from pyramid.threadlocal import get_current_registry as get_current_registry

NO_PERMISSION_REQUIRED: str

def remember(request, userid, **kw): ...
def forget(request, **kw): ...
def principals_allowed_by_permission(context, permission): ...
def view_execution_permitted(context, request, name: str = ''): ...

class PermitsResult(int):
    def __new__(cls, s, *args): ...
    @property
    def msg(self): ...

class Denied(PermitsResult):
    boolval: int

class Allowed(PermitsResult):
    boolval: int

class SecurityAPIMixin:
    @property
    def identity(self): ...
    @property
    def authenticated_userid(self): ...
    @property
    def is_authenticated(self): ...
    def has_permission(self, permission, context: Incomplete | None = None): ...

class AuthenticationAPIMixin:
    @property
    def unauthenticated_userid(self): ...
    unauthenticated_userid: Incomplete
    @property
    def effective_principals(self): ...
    effective_principals: Incomplete

class LegacySecurityPolicy:
    def identity(self, request): ...
    def authenticated_userid(self, request): ...
    def remember(self, request, userid, **kw): ...
    def forget(self, request, **kw): ...
    def permits(self, request, context, permission): ...

Everyone: str
Authenticated: str
Allow: str
Deny: str

class AllPermissionsList:
    def __iter__(self): ...
    def __contains__(self, other) -> bool: ...
    def __eq__(self, other): ...

ALL_PERMISSIONS: Incomplete
DENY_ALL: Incomplete

class ACLPermitsResult(PermitsResult):
    def __new__(cls, ace, acl, permission, principals, context): ...

class ACLDenied(ACLPermitsResult, Denied): ...
class ACLAllowed(ACLPermitsResult, Allowed): ...