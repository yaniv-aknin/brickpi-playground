#!/usr/bin/env python3
import curses
import sys
import reactor
import cursesctrlr
import time
try:
    import brickpictrlr
except ImportError:
    print("no brickpi3")

commands = {}
def command(func):
    commands[func.__name__] = func
    return func

@command
def curses():
    r = reactor.Reactor()
    r.controllers['curses'] = cursesctrlr.CursesController(r)
    with r:
        r.curses.set_key('q', lambda: r.stop())
        r.schedule_recurring(5, lambda: r.log('%.3f' % time.time()))
        r.loop()

@command
def robot():
    r = reactor.Reactor()
    r.controllers['curses'] = cursesctrlr.CursesController(r)
    r.controllers['brick'] = brickpictrlr.BrickController(r)
    with r:
        r.curses.set_key('q', lambda: r.stop())
        r.brick.new_motor(r.brick.PORT_B, 'left')
        r.brick.new_motor(r.brick.PORT_B, 'right')
        r.curses.set_key(curses.KEY_UP, lambda: r.brick.motors.all.set_power(50))
        r.curses.set_key(curses.KEY_DOWN, lambda: r.brick.motors.all.set_power(-50))
        r.curses.set_key(' ', lambda: r.brick.motors.all.float())
        r.loop()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit("usage: %s <%s>" % (sys.argv[0], "|".join(commands)))
    commands[sys.argv[1]]()
