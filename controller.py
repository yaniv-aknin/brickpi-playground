import curses
import time
 
class BaseController(object):
    def __enter__(self):
        self.screen = curses.initscr() # get the curses screen window
        curses.noecho() # turn off input echoing
        curses.cbreak() # respond to keys immediately (don't wait for enter)
        self.screen.keypad(True) # map arrow keys to special values
        curses.curs_set(False)
        self.screen.nodelay(True)
        self.running = True
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
    def __init__(self):
        self.handlers = []
        self.DISPATCH =  {
            curses.KEY_RIGHT: self.right,
            curses.KEY_LEFT: self.left,
            curses.KEY_UP: self.up,
            curses.KEY_DOWN: self.down,
        }
    def addstr(self, y, x, text, ljust=0):
        self.screen.addstr(y, x, text.ljust(ljust))
        self.screen.noutrefresh()
        curses.doupdate()
    def logger(self, y=0):
        return lambda text: self.addstr(y, 0, text, 70)
    def loop(self):
        previous = time.time()
        while self.running:
            time.sleep(0.1)
            char = self.screen.getch()
            if char != -1:
                self.keypress(char)
            for handler in self.handlers:
                handler()
            current = time.time()
            self.addstr(2, 0, 'ts: %d, delay: %.2f' % (current, (current - previous),))
            previous = current
    def keypress(self, char):
        if char == ord('q'):
            self.running = False
            return
        try:
            self.DISPATCH[char]()
        except KeyError:
            self.unknown_key(char)
    def unknown_key(self, char):
        self.addstr(1, 0, 'unknown key %r' % (chr(char),))
    def right(self):
        self.addstr(0, 0, 'right', 5)
    def left(self):
        self.addstr(0, 0, 'left', 5)
    def up(self):
        self.addstr(0, 0, 'up', 5)
    def down(self):
        self.addstr(0, 0, 'down', 5)

class Controller(BaseController):
    pass
