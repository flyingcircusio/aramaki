from _typeshed import Incomplete
from zope.interface import Interface as Interface, classImplements as classImplements
from zope.interface.interface import InterfaceClass as InterfaceClass, fromFunction as fromFunction

class optional:
    __doc__: Incomplete
    def __init__(self, method) -> None: ...

class ABCInterfaceClass(InterfaceClass):
    __class__: Incomplete
    def __init__(self, name, bases, attrs) -> None: ...
    def getABC(self): ...
    def getRegisteredConformers(self): ...

ABCInterface: Incomplete
