from _typeshed import Incomplete

__all__ = ['open', 'stdin', 'stdout', 'stderr', 'stdin_bytes', 'stdout_bytes', 'stderr_bytes']

sync_open = open

def open(file, mode: str = 'r', buffering: int = -1, encoding: Incomplete | None = None, errors: Incomplete | None = None, newline: Incomplete | None = None, closefd: bool = True, opener: Incomplete | None = None, *, loop: Incomplete | None = None, executor: Incomplete | None = None): ...

stdin: Incomplete
stdout: Incomplete
stderr: Incomplete
stdin_bytes: Incomplete
stdout_bytes: Incomplete
stderr_bytes: Incomplete
