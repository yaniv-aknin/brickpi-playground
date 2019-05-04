#!/usr/bin/env python3
import curses
import sys
import cursesctrlr
import time
import twowheelctrlr
import robocore
try:
    import brickpictrlr
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
        curses.set_key('q', core.stop)
        core.schedule_recurring(5, lambda: core.log('%.3f' % time.time()))
        core.run()

@command
def robot():
    core = robocore.RoboCore()
    console = core.install('console', cursesctrlr.CursesController)
    brick = core.install('brick', brickpictrlr.BrickController)
    with core:
        console.set_key('q', core.stop)
        brick.new_motor(brick.PORT_D, 'left')
        brick.new_motor(brick.PORT_C, 'right')
        console.set_key(curses.KEY_UP, lambda: brick.motors.all.set_power(50))
        console.set_key(curses.KEY_DOWN, lambda: brick.motors.all.set_power(-50))
        console.set_key(' ', brick.motors.all.float)
        core.run()

@command
def twowheel():
    def slow_on_distance(distance, core):
        twowheel = core.controllers['twowheel']
        if distance < 30:
            twowheel.speed = min(twowheel.speed, 20)
    core = robocore.RoboCore()
    console = core.install('console', cursesctrlr.CursesController)
    brick = core.install('brick', brickpictrlr.BrickController)
    twowheel = core.install('twowheel', twowheelctrlr.TwoWheelController, right_port=brick.PORT_C, left_port=brick.PORT_D)
    with core:
        console.set_key('q', core.stop)
        brick.new_sensor(brickpictrlr.DistanceSensor, brick.PORT_3, visible=True, callback=slow_on_distance)
        brick.new_sensor(brickpictrlr.CompassSensor, brick.PORT_4, visible=True)
        brick.new_sensor(brickpictrlr.SoundSensor, brick.PORT_2, name='leftsound', visible=True)
        brick.new_sensor(brickpictrlr.SoundSensor, brick.PORT_1, name='rightsound', visible=True)
        time.sleep(0.2) # let distance sensors settle; http://tiny.cc/13z65y
        core.run()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit("usage: %s <%s>" % (sys.argv[0], "|".join(commands)))
    commands[sys.argv[1]]()
