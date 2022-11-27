import inspect
import sys
import threading


def is_classmethod(method):
    # Abbreviated form of https://stackoverflow.com/a/19228282
    return inspect.ismethod(method) and isinstance(method.__self__, type)


class LocalContext(threading.local):
    def __init__(self):
        self.stack = []

    @property
    def current(self):
        return self.stack[-1]


class ApplicationContextManager:
    def __init__(self, context_factory):
        self.active_contexts = LocalContext()
        self.context_factory = context_factory

        self.event_handlers = {}

    def bind(self, **kw):
        return self.context_factory(self, **kw)

    def push(self, context):
        stack = self.active_contexts.stack
        if context in stack:
            raise RuntimeError("{context} is already active.")
        stack.append(context)

    def pop(self, context):
        stack = self.active_contexts.stack
        if context is not self.active_contexts.current:
            raise RuntimeError("{context} is not on the top of the stack.")
        del stack[-1]

    def handle(self, event_name):
        def handle_decorator(func):
            self.event_handlers.setdefault(event_name, [])
            self.event_handlers[event_name].append(func)
            return func

        return handle_decorator

    def __getattr__(self, name):
        try:
            unbound = getattr(self.context_factory, name)
        except AttributeError:
            pass
        else:
            if is_classmethod(unbound):
                return unbound
        return getattr(self.active_contexts.current, name)


class AbstractApplicationContext:
    def __init__(self, manager, **kw):
        self.manager = manager
        self.bind(**kw)

    def bind(self):
        pass

    def notify(self, event, *args, **kwargs):
        self.events.append((event, args, kwargs))

    @classmethod
    def setup(cls):
        return ApplicationContextManager(cls)

    def __enter__(self):
        self.manager.push(self)
        self.events = []
        self.enter()

    def _handle_events_first_phase(self):
        second_phase_events = []
        while self.events:
            event, args, kw = self.events.pop(0)
            for handler in self.manager.event_handlers.get(event, []):
                result = handler(*args, **kw)
                if not inspect.isgenerator(result):
                    continue
                # Running the first phase of a generator
                # requires an initial next call
                next(result)
                second_phase_events.append(result)
        return second_phase_events

    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        if exc_type:
            self.exit(exc_type, exc_value, exc_tb)
            self.manager.pop(self)
            return

        try:
            second_phase_events = self._handle_events_first_phase()
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.exit(exc_type, exc_value, exc_tb)
            self.manager.pop(self)
            raise

        self.exit()

        while second_phase_events:
            handler = second_phase_events.pop(0)
            self.enter()
            try:
                next(handler)
            except StopIteration:
                pass
            except Exception:
                # XXX retry and logging
                self.exit(*sys.exc_info())
            else:
                self.exit()
            # It's currently not clear whether handling this depth-first
            # or breadth-first is to be preferred. Depth-first is more
            # convenient to implement right now.
            second_phase_events.extend(self._handle_events_first_phase())

        self.manager.pop(self)
