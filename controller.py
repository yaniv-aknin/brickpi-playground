import curses
 
class BaseController(object):
    def __enter__(self):
        self.screen = curses.initscr() # get the curses screen window
        curses.noecho() # turn off input echoing
        curses.cbreak() # respond to keys immediately (don't wait for enter)
        self.screen.keypad(True) # map arrow keys to special values
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
    def addstr(self, y, x, text, ljust=0):
        self.screen.addstr(y, x, text.ljust(ljust))
        self.screen.noutrefresh()
        curses.doupdate()
    def logger(self, y=0):
        return lambda text: self.addstr(y, 0, text, 70)
    def loop(self):
        DISPATCH = {
            curses.KEY_RIGHT: self.right,
            curses.KEY_LEFT: self.left,
            curses.KEY_UP: self.up,
            curses.KEY_DOWN: self.down,
        }
        while True:
            char = self.screen.getch()
            if char == ord('q'):
                break
            DISPATCH.get(char, self.unknown_key)()
    def unknown_key(self):
        pass
    def right(self):
        self.screen.addstr(0, 0, 'right', 5)
    def left(self):
        self.screen.addstr(0, 0, 'left', 5)
    def up(self):
        self.screen.addstr(0, 0, 'up', 5)
    def down(self):
        self.screen.addstr(0, 0, 'down', 5)

class Controller(BaseController):
    pass
