import curses
import time

class CursesController(object):
    def __init__(self, reactor):
        self.reactor = reactor
        self.dispatch = {}
    def __enter__(self):
        self.screen = curses.initscr() # get the curses screen window
        curses.noecho() # turn off input echoing
        curses.cbreak() # respond to keys immediately (don't wait for enter)
        self.screen.keypad(True) # map arrow keys to special values
        curses.curs_set(False)
        self.screen.nodelay(True)
        self.reactor.loggers.append(self.logger)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
    def addstr(self, y, x, text, ljust=70): # TODO: replace 70 with screen width
        self.screen.addstr(y, x, text.ljust(ljust))
        self.screen.noutrefresh()
        curses.doupdate()
    def logger(self, text):
        return self.addstr(0, 0, text)
    def formatter(self, obj):
        if hasattr(obj, 'formatter'):
            return obj.formatter()
        elif isinstance(obj, float):
            return '%.2f' % (obj,)
        else:
            return str(obj)
    def __call__(self):
        self.dispatch_keyboard()
        self.draw_variables(self.reactor.variables)
    def dispatch_keyboard(self):
        char = self.screen.getch()
        if char != -1:
            try:
                self.dispatch[char]()
            except KeyError:
                self.unknown_key(char)
    def draw_variables(self, variables):
        for index, (name, value) in enumerate(sorted(variables.items())):
            self.addstr(index+1, 0, '%s: %s' % (name, self.formatter(value)))
    def unknown_key(self, char):
        try:
            char = chr(char)
        except ValueError:
            pass
        self.reactor.log('unknown key: %r' % (char,))
    def set_key(self, key, func):
        if isinstance(key, str):
            key = ord(key)
        self.dispatch[key] = func
