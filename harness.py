#!/usr/bin/env python3
import curses
import sys
import cursesctrlr
import time
import twowheelctrlr
import robocore
try:
    import brickpictrlr
    import scanctrlr
except ImportError:
    print("no brickpi3")

commands = {}
def command(func):
    commands[func.__name__] = func
    return func

@command
def console():
    core = robocore.RoboCore()
    console = core.install('console', cursesctrlr.CursesController)
    with core:
        console.set_key('q', core.stop)
        core.recurring(5, lambda: core.log('%.3f' % time.time()))
        core.run()

@command
def twowheel():
    core = robocore.RoboCore()
    console = core.install('console', cursesctrlr.CursesController)
    brick = core.install('brick', brickpictrlr.BrickController)
    twowheel = core.install('twowheel', twowheelctrlr.TwoWheelController, right_port=brick.PORT_C, left_port=brick.PORT_D)
    with core:
        console.set_key('q', core.stop)
        core.run()

@command
def scanner():
    core = robocore.RoboCore()
    console = core.install('console', cursesctrlr.CursesController)
    brick = core.install('brick', brickpictrlr.BrickController)
    twowheel = core.install('twowheel', twowheelctrlr.TwoWheelController, right_port=brick.PORT_C, left_port=brick.PORT_D)
    scanner = core.install('scanner', scanctrlr.ScanController, left_sound_port=brick.PORT_2, right_sound_port=brick.PORT_1, compass_port=brick.PORT_4)
    with core:
        console.set_key('q', core.stop)
        time.sleep(0.2) # let distance sensors settle; http://tiny.cc/13z65y
        core.run()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit("usage: %s <%s>" % (sys.argv[0], "|".join(commands)))
    commands[sys.argv[1]]()
