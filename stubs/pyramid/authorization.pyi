from _typeshed import Incomplete
from pyramid.interfaces import IAuthorizationPolicy as IAuthorizationPolicy
from pyramid.location import lineage as lineage
from pyramid.security import ACLAllowed as _ACLAllowed, ACLDenied as _ACLDenied, AllPermissionsList as _AllPermissionsList, Allow as Allow, Authenticated as Authenticated, Deny as Deny, Everyone as Everyone
from pyramid.util import is_nonstr_iter as is_nonstr_iter

Everyone = Everyone
Authenticated = Authenticated
Allow = Allow
Deny = Deny

class AllPermissionsList(_AllPermissionsList): ...
class ACLAllowed(_ACLAllowed): ...
class ACLDenied(_ACLDenied): ...

ALL_PERMISSIONS: Incomplete
DENY_ALL: Incomplete

class ACLAuthorizationPolicy:
    helper: Incomplete
    def __init__(self) -> None: ...
    def permits(self, context, principals, permission): ...
    def principals_allowed_by_permission(self, context, permission): ...

class ACLHelper:
    def permits(self, context, principals, permission): ...
    def principals_allowed_by_permission(self, context, permission): ...
