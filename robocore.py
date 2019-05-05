import collections
import asyncio

class BaseController(object):
    FREQUENCY_SECONDS = 0.1
    REQUIREMENTS = set()
    def __init__(self, core):
        self.core = core
        if not self.REQUIREMENTS.issubset(set(core.controllers)):
            missing = self.REQUIREMENTS - set(core.controllers)
            raise RuntimeError("missing controllers: %s" % ", ".join(missing))
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class RoboCore(object):
    FREQUENCY_SECONDS = 0.1
    def __init__(self, frequency_seconds=0.1, loop=None):
        self.frequency_seconds = frequency_seconds
        self.loop = loop or asyncio.get_event_loop()
        self.controllers = collections.OrderedDict()
        self.variables = {}
        self.loggers = []
        self.contexts = None
    def __enter__(self):
        self.contexts = collections.OrderedDict()
        for name, controller in self.controllers.items():
            self.contexts[name] = controller.__enter__()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        for name, handle in self.contexts.items():
            handle.__exit__(exc_type, exc_val, exc_tb)
        self.contexts = None
    def log(self, text):
        for logger in self.loggers:
            logger(text)
    def run(self):
        def update_timestamp():
            self.variables['timestamp'] = self.loop.time()
        self.recurring(self.FREQUENCY_SECONDS, update_timestamp)
        self.loop.run_forever()
    def install(self, name, controller_class, *args, **kwargs):
        controller = controller_class(self, *args, **kwargs)
        self.controllers[name] = controller
        if controller.FREQUENCY_SECONDS is not None:
            self.recurring(controller.FREQUENCY_SECONDS, controller)
        return controller
    def recurring(self, interval, func, *args, **kwargs):
        def scheduled():
            func(*args, **kwargs)
            self.loop.call_later(interval, scheduled)
        self.loop.call_soon(scheduled)
    def stop(self):
        self.loop.stop()
