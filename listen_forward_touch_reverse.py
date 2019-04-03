#!/usr/bin/env python

import sys
import brickpi3
import time
import atexit

BP = brickpi3.BrickPi3()
BP.reset_all()
atexit.register(BP.reset_all)
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

def listen():
    sound = BP.get_sensor(BP.PORT_3)[0]
    sys.stderr.write('\rsound: %d   ' % (sound,))
    return sound

def distance():
    distance = BP.get_sensor(BP.PORT_1)
    sys.stderr.write('\rdistance: %d   ' % (distance,))
    return distance

def go():
    while True:
        print 'listening'
        while True:
            time.sleep(0.1)
            if listen() < 1000:
                sys.stderr.write('\n')
                break
        print 'driving'
        motors(100)
        while True:
            time.sleep(0.1)
            if distance() < 40:
                motors(40)
                sys.stderr.write('\n')
                break
        while True:
            if touch():
                print 'touched'
                break
            time.sleep(0.1)
        motors(-40)
        time.sleep(3)
        motors(0)

if __name__ == '__main__':
    go()
