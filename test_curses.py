import reactor
import cursesctrlr

r = reactor.Reactor()
r.controllers['curses'] = cursesctrlr.CursesController(r)
with r:
    r.loop()
