import brickpi3
import atexit
import os

class Bag(dict):
    def __getattr__(self, name):
        return self[name]

class BrickController(object):
    PORT_1 = brickpi3.BrickPi3.PORT_1
    PORT_2 = brickpi3.BrickPi3.PORT_2
    PORT_3 = brickpi3.BrickPi3.PORT_3
    PORT_4 = brickpi3.BrickPi3.PORT_4
    PORT_A = brickpi3.BrickPi3.PORT_A
    PORT_B = brickpi3.BrickPi3.PORT_B
    PORT_C = brickpi3.BrickPi3.PORT_C
    PORT_D = brickpi3.BrickPi3.PORT_D
    SENSOR_TYPE = brickpi3.BrickPi3.SENSOR_TYPE
    SENSOR_CUSTOM = brickpi3.BrickPi3.SENSOR_CUSTOM
    MOTOR_FLOAT = brickpi3.BrickPi3.MOTOR_FLOAT
    def __init__(self, reactor):
        self.reactor = reactor
        self.sensors = Bag()
        self.motors = Bag()
    def __enter__(self):
        self.device = brickpi3.BrickPi3()
        self.device.reset_all()
        atexit.register(self.device.reset_all)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.reset_all()
    def new_motor(self, port, name):
        motor = Motor(self, port, name)
        self.motors[motor.name] = motor
        if 'all' not in self.motors:
            self.motors['all'] = MotorSet(motor.brick, motor.port, 'all')
        else:
            self.motors.all.add_port(motor.port)
    def __call__(self):
        pass

class MotorBase(object):
    def __init__(self, brick, port, name):
        self.brick = brick
        self.port = port
        self.name = name
    def float(self):
        self.set_power(self.brick.MOTOR_FLOAT)
    def stop(self):
        self.set_power(0)
    def set_power(self, power):
        if 'BRICKPI_DRYRUN' not in os.environ:
            self.brick.device.set_motor_power(self.port, power)

class Motor(MotorBase):
    pass

class MotorSet(MotorBase):
    def add_port(self, port):
        self.port += port

class BaseSensor(object):
    def __init__(self, brick, port):
        self.brick = brick
        self.port = port
        self.brick.set_sensor_type(port, *self.SENSOR_TYPE)
    def __call__(self):
        return self.brick.get_sensor(self.port)

class TouchSensor(BaseSensor):
    SENSOR_TYPE = (BrickController.SENSOR_TYPE.TOUCH,)
class DistanceSensor(BaseSensor):
    SENSOR_TYPE = (BrickController.SENSOR_TYPE.NXT_ULTRASONIC,)
class SoundSensor(BaseSensor):
    SENSOR_TYPE = (BrickController.SENSOR_TYPE.CUSTOM, [(BrickController.SENSOR_CUSTOM.PIN1_ADC)])
