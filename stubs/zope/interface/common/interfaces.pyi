from zope.interface import Interface as Interface, classImplements as classImplements

class IException(Interface): ...
class IStandardError(IException): ...
class IWarning(IException): ...
class ISyntaxError(IStandardError): ...
class ILookupError(IStandardError): ...
class IValueError(IStandardError): ...
class IRuntimeError(IStandardError): ...
class IArithmeticError(IStandardError): ...
class IAssertionError(IStandardError): ...
class IAttributeError(IStandardError): ...
class IDeprecationWarning(IWarning): ...
class IEOFError(IStandardError): ...
class IEnvironmentError(IStandardError): ...
class IFloatingPointError(IArithmeticError): ...
class IIOError(IEnvironmentError): ...
class IImportError(IStandardError): ...
class IIndentationError(ISyntaxError): ...
class IIndexError(ILookupError): ...
class IKeyError(ILookupError): ...
class IKeyboardInterrupt(IStandardError): ...
class IMemoryError(IStandardError): ...
class INameError(IStandardError): ...
class INotImplementedError(IRuntimeError): ...
class IOSError(IEnvironmentError): ...
class IOverflowError(IArithmeticError): ...
class IOverflowWarning(IWarning): ...
class IReferenceError(IStandardError): ...
class IRuntimeWarning(IWarning): ...
class IStopIteration(IException): ...
class ISyntaxWarning(IWarning): ...
class ISystemError(IStandardError): ...
class ISystemExit(IException): ...
class ITabError(IIndentationError): ...
class ITypeError(IStandardError): ...
class IUnboundLocalError(INameError): ...
class IUnicodeError(IValueError): ...
class IUserWarning(IWarning): ...
class IZeroDivisionError(IArithmeticError): ...
