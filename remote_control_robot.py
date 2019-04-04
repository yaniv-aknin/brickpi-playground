import sys
import time
import brickpiplus
import controller

BP = brickpiplus.GetBrickHandle()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.CUSTOM,
                   [(BP.SENSOR_CUSTOM.PIN1_ADC)])
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)

def motors(power=-128):
    BP.set_motor_power(BP.PORT_D + BP.PORT_B, power)

def turn(motor):
    BP.set_motor_power(motor, 30)

class Controller(controller.Controller):
    def __init__(self):
        super(Controller, self).__init__()
        self.speed = 40
        self.direction = 1
        self.DISPATCH[ord(' ')] = self.stop
        self.DISPATCH[ord('+')] = self.faster
        self.DISPATCH[ord('-')] = self.slower
        self.handlers.append(self.slow_down_on_distance)
        self.handlers.append(self.stop_on_touch)
    def set_speed(self, speed):
        self.speed = min(max(speed, 10), 70)
        self.addstr(3, 0, "speed: %d" % (self.speed,), 30)
        if not self.is_idle:
            motors(self.direction * self.speed)
    @property
    def is_idle(self):
        return BP.get_motor_status(BP.PORT_D)[-1] == BP.get_motor_status(BP.PORT_B)[-1] == 0
    def faster(self):
        self.set_speed(self.speed + 10)
    def slower(self):
        self.set_speed(self.speed - 10)
    def right(self):
        turn(BP.PORT_B)
    def left(self):
        turn(BP.PORT_D)
    def up(self):
        self.direction = 1
        if self.is_idle:
            motors(self.direction * self.speed)
        self.set_speed(self.speed)
    def down(self):
        self.direction = -1
        if self.is_idle:
            motors(self.direction * self.speed)
        self.set_speed(self.speed)
    def stop(self):
        motors(-128)
    def slow_down_on_distance(self):
        distance = BP.get_sensor(BP.PORT_1)
        self.addstr(4, 0, "distance: %d" % (distance,), 40)
        if distance < 40:
            self.set_speed(min(self.speed, 30))
    def stop_on_touch(self):
        touching = BP.get_sensor(BP.PORT_4)
        self.addstr(5, 0, "touch: %s" % (touching,), 40)
        if touching:
            motors(0)

with Controller() as ctrl:
    ctrl.loop()
