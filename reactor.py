import time

class Reactor(object):
    def __enter__(self):
        self.handles = {}
        for name, controller in self.controllers.items():
            self.handles[name] = controller.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name, handle in self.handles.items():
            handle.__exit__(exc_type, exc_val, exc_tb)
        self.handles = None

    def __init__(self, delay=0.1):
        self.delay = 0.1
        self.controllers = {}
        self.variables = {}
        self.loggers = []
        self.handles = None

    def __getattr__(self, name):
        return self.handles[name]

    def loop(self):
        self.variables['delay'] = 0
        assert self.handles is not None
        previous = time.time()
        self.running = True
        while self.running:
            time.sleep(self.delay)
            for name, handle in self.handles.items():
                handle()
            current = time.time()
            self.variables['delay'] = current - previous
            self.variables['timestamp'] = current
            previous = current

    def log(self, text):
        for logger in self.loggers:
            logger(text)
