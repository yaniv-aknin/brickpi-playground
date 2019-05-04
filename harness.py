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
        if distance < 40:
            core.twowheel.speed = min(core.twowheel.speed, 20)
    def stop_on_sound(sound, core):
        if sound < 1000:
            core.twowheel.stop()
    core = robocore.RoboCore()
    console = core.install('console', cursesctrlr.CursesController)
    brick = core.install('brick', brickpictrlr.BrickController)
    twowheel = core.install('twowheel', twowheelctrlr.TwoWheelController, right_port=brick.PORT_C, left_port=brick.PORT_D)
    with core:
        console.set_key('q', core.stop)
    #    brick.new_sensor(brickpictrlr.DistanceSensor, brick.PORT_1, visible=True, callback=slow_on_distance)
    #    brick.new_sensor(brickpictrlr.SoundSensor, brick.PORT_3, visible=True, callback=stop_on_sound)
        core.run()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit("usage: %s <%s>" % (sys.argv[0], "|".join(commands)))
    commands[sys.argv[1]]()
