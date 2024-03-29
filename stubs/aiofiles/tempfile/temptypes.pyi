from ..base import AsyncBase as AsyncBase
from ..threadpool.utils import cond_delegate_to_executor as cond_delegate_to_executor, delegate_to_executor as delegate_to_executor, proxy_property_directly as proxy_property_directly

class AsyncSpooledTemporaryFile(AsyncBase):
    async def write(self, s): ...
    async def writelines(self, iterable): ...

class AsyncTemporaryDirectory:
    def __init__(self, file, loop, executor) -> None: ...
    async def close(self) -> None: ...
