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
            self.motors['all'] = MotorSet('all', motor)
        else:
            self.motors.all.add_motor(motor)
        return motor
    def new_motor_set(self, name, first_motor, *remaining_motors):
        return MotorSet(name, first_motor, *remaining_motors)
    def new_sensor(self, kind, port, name=None, visible=False, callback=lambda v, r: None, interval=0.1):
        name = name or kind.__name__
        sensor = kind(self, port)
        if visible:
            def wrapper(sensor):
                def callable():
                    value = self.reactor.variables[name] = sensor()
                    return value
                return callable
            sensor = wrapper(sensor)
        self.sensors[name] = sensor
        if interval:
            self.reactor.schedule_recurring(interval, lambda: callback(sensor(), self.reactor))
        return sensor
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
    def __init__(self, name, first_motor, *remaining_motors):
        self.name = name
        self.motors = [first_motor]
        self.brick = first_motor.brick
        for motor in remaining_motors:
            self.add_motor(motor)
    def add_motor(self, motor):
        if self.brick != motor.brick:
            raise NotImplementedError("all motors must belong to the same brick")
        self.motors.append(motor)
    @property
    def port(self):
        return sum(motor.port for motor in self.motors)

class BaseSensor(object):
    def __init__(self, brick, port):
        self.brick = brick
        self.port = port
        self.brick.device.set_sensor_type(port, *self.SENSOR_TYPE)
    def __call__(self):
        return self.brick.device.get_sensor(self.port)

class TouchSensor(BaseSensor):
    SENSOR_TYPE = (BrickController.SENSOR_TYPE.TOUCH,)
class DistanceSensor(BaseSensor):
    SENSOR_TYPE = (BrickController.SENSOR_TYPE.NXT_ULTRASONIC,)
class SoundSensor(BaseSensor):
    SENSOR_TYPE = (BrickController.SENSOR_TYPE.CUSTOM, [(BrickController.SENSOR_CUSTOM.PIN1_ADC)])
    def __call__(self):
        return super(SoundSensor, self).__call__()[0]
