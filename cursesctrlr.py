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
    def __call__(self):
        char = self.screen.getch()
        if char != -1:
            if char == ord('q'):
                self.reactor.running = False
                return
            try:
                self.dispatch[char]()
            except KeyError:
                self.unknown_key(char)
        for index, (name, value) in enumerate(sorted(self.reactor.variables.items())):
            FORMATS = {
                float: '%.2f',
            }
            value = FORMATS.get(type(value), '%s') % (value,)
            self.addstr(index+1, 0, '%s: %s' % (name, value))
    def unknown_key(self, char):
        pass
