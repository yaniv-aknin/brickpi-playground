import collections
import asyncio

class RoboCore(object):
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
        self.loop.call_soon(self.control)
        self.loop.run_forever()
    def control(self):
        self.variables['timestamp'] = self.loop.time()
        for controller in self.controllers.values():
            controller()
        self.loop.call_later(self.frequency_seconds, self.control)
    def install(self, name, controller_class, *args, **kwargs):
        controller = controller_class(self, *args, **kwargs)
        self.controllers[name] = controller
        return controller
    def schedule_once(self, delay, func):
        return self.loop.call_later(delay, func)
    def schedule_recurring(self, interval, func):
        def scheduled():
            func()
            self.loop.call_later(interval, scheduled)
        self.loop.call_soon(scheduled)
    def stop(self):
        self.loop.stop()
