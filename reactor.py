import heapq
import collections
import time

class Reactor(object):
    def __enter__(self):
        self.handles = collections.OrderedDict()
        for name, controller in self.controllers.items():
            self.handles[name] = controller.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name, handle in self.handles.items():
            handle.__exit__(exc_type, exc_val, exc_tb)
        self.handles = None

    def __init__(self, delay=0.1):
        self.delay = 0.1
        self.controllers = collections.OrderedDict()
        self.variables = {}
        self.loggers = []
        self.timers = []
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
            while self.timers and heapq.nsmallest(1, self.timers)[0][0] < current:
                when, interval, func = heapq.heappop(self.timers)
                func()
                if interval:
                    self.schedule_recurring(interval, func)
            self.variables['delay'] = current - previous
            self.variables['timestamp'] = current
            previous = current

    def log(self, text):
        for logger in self.loggers:
            logger(text)

    def stop(self):
        self.running = False

    def schedule_once(self, duration, func):
        when = time.time() + duration
        heapq.heappush(self.timers, (when, 0, func))

    def schedule_recurring(self, interval, func):
        when = time.time() + interval
        heapq.heappush(self.timers, (when, interval, func))
