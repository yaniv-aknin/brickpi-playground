#!/usr/bin/env python

import brickpi3
import time

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.CUSTOM, [(BP.SENSOR_CUSTOM.PIN1_ADC)])

time.sleep(1)

def motors(power=0):
    BP.set_motor_power(BP.PORT_D + BP.PORT_B, power)

def touch():
    return BP.get_sensor(BP.PORT_4)

def listen():
    return BP.get_sensor(BP.PORT_3)[0]

    
try:
    print 'listening'
    while True:
        if listen() < 1000:
            break
        time.sleep(0.1)
    print 'driving'
    motors(40)
    while True:
        if touch():
            print 'touched'
            break
        time.sleep(0.1)
    motors(-20)
    time.sleep(1)
finally:
    motors()
    print 'done'
