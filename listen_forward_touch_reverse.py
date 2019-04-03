#!/usr/bin/env python

import sys
import time
import brickpiplus
import controller

BP = brickpiplus.GetBrickHandle()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.CUSTOM,
                   [(BP.SENSOR_CUSTOM.PIN1_ADC)])
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)

def motors(power=0):
    BP.set_motor_power(BP.PORT_D + BP.PORT_B, power)

def turn(motor):
    BP.set_motor_power(motor, 30)
    time.sleep(2)
    motors()

def right():
    turn(BP.PORT_B)

def left():
    turn(BP.PORT_D)

def touch():
    return BP.get_sensor(BP.PORT_4)

def listen(logger):
    sound = BP.get_sensor(BP.PORT_3)[0]
    logger('sound: %d' % (sound,))
    return sound

def distance(logger):
    distance = BP.get_sensor(BP.PORT_1)
    logger('distance: %d' % (distance,))
    return distance

def go():
    with controller.Controller() as ctrl:
        logger = ctrl.logger()
        while True:
            logger('listening')
            while True:
                time.sleep(0.1)
                if listen(logger) < 1000:
                    break
            logger('driving')
            motors(100)
            while True:
                time.sleep(0.1)
                if distance(logger) < 40:
                    motors(40)
                    break
            while True:
                if touch():
                    logger('touched')
                    break
                time.sleep(0.1)
            motors(-40)
            time.sleep(3)
            motors(0)

if __name__ == '__main__':
    go()
