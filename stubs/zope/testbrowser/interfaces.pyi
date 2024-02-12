import zope.interface
import zope.interface.common.mapping
from _typeshed import Incomplete

__docformat__: str

class AlreadyExpiredError(ValueError): ...

class ICookies(zope.interface.common.mapping.IExtendedReadMapping, zope.interface.common.mapping.IExtendedWriteMapping, zope.interface.common.mapping.IMapping):
    url: Incomplete
    header: Incomplete
    def forURL(url) -> None: ...
    def getinfo(name) -> None: ...
    def iterinfo(name: Incomplete | None = None) -> None: ...
    def create(name, value, domain: Incomplete | None = None, expires: Incomplete | None = None, path: Incomplete | None = None, secure: Incomplete | None = None, comment: Incomplete | None = None, commenturl: Incomplete | None = None, port: Incomplete | None = None) -> None: ...
    def change(name, value: Incomplete | None = None, domain: Incomplete | None = None, expires: Incomplete | None = None, path: Incomplete | None = None, secure: Incomplete | None = None, comment: Incomplete | None = None, commenturl: Incomplete | None = None, port: Incomplete | None = None) -> None: ...
    def clearAll() -> None: ...
    def clearAllSession() -> None: ...

class IBrowser(zope.interface.Interface):
    cookies: Incomplete
    url: Incomplete
    headers: Incomplete
    contents: Incomplete
    isHtml: Incomplete
    title: Incomplete
    handleErrors: Incomplete
    followRedirects: Incomplete
    def addHeader(key, value) -> None: ...
    def open(url, data: Incomplete | None = None) -> None: ...
    def reload() -> None: ...
    def goBack(count: int = 1) -> None: ...
    def getLink(text: Incomplete | None = None, url: Incomplete | None = None, id: Incomplete | None = None, index: int = 0) -> None: ...
    lastRequestSeconds: Incomplete
    def getControl(label: Incomplete | None = None, name: Incomplete | None = None, index: Incomplete | None = None) -> None: ...
    def getForm(id: Incomplete | None = None, name: Incomplete | None = None, action: Incomplete | None = None, index: Incomplete | None = None) -> None: ...

class ExpiredError(Exception): ...

class IControl(zope.interface.Interface):
    name: Incomplete
    value: Incomplete
    type: Incomplete
    disabled: Incomplete
    multiple: Incomplete
    def clear() -> None: ...

class IListControl(IControl):
    options: Incomplete
    displayOptions: Incomplete
    displayValue: Incomplete
    def getControl(label: Incomplete | None = None, value: Incomplete | None = None, index: Incomplete | None = None) -> None: ...
    controls: Incomplete

class ISubmitControl(IControl):
    def click() -> None: ...

class IImageSubmitControl(ISubmitControl):
    def click(coord=(1, 1)) -> None: ...

class IItemControl(zope.interface.Interface):
    control: Incomplete
    disabled: Incomplete
    selected: Incomplete
    optionValue: Incomplete

class ILink(zope.interface.Interface):
    def click() -> None: ...
    url: Incomplete
    attrs: Incomplete
    text: Incomplete
    tag: Incomplete

class IForm(zope.interface.Interface):
    action: Incomplete
    method: Incomplete
    enctype: Incomplete
    name: Incomplete
    id: Incomplete
    def getControl(label: Incomplete | None = None, name: Incomplete | None = None, index: Incomplete | None = None) -> None: ...
    def submit(label: Incomplete | None = None, name: Incomplete | None = None, index: Incomplete | None = None, coord=(1, 1)) -> None: ...
