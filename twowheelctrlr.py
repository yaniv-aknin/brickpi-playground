import curses
import enum

class Steer(enum.Enum):
    left = 1
    none = 2
    right = 3

class TwoWheelController(object):
    def __init__(self, reactor, left_port, right_port):
        if {'curses', 'brick'} & set(reactor.controllers) != {'curses', 'brick'}:
            raise RuntimeError('need curses and brick controllers')
        self.reactor = reactor
        self.left_port = left_port
        self.right_port = right_port
    def __enter__(self):
        self.left_motor = self.reactor.brick.new_motor(self.left_port, 'left')
        self.right_motor = self.reactor.brick.new_motor(self.right_port, 'right')
        self.both_motors = self.reactor.brick.new_motor_set('both', self.left_motor, self.right_motor)
        self.reactor.curses.set_key(curses.KEY_UP, self.forward)
        self.reactor.curses.set_key(curses.KEY_DOWN, self.reverse)
        self.reactor.curses.set_key(curses.KEY_LEFT, self.left)
        self.reactor.curses.set_key(curses.KEY_RIGHT, self.right)
        self.reactor.curses.set_key(' ', self.stop)
        self.reactor.curses.set_key('+', self.faster)
        self.reactor.curses.set_key('-', self.slower)
        self.driving = False
        self.direction = 1
        self.speed = 40
        self.steer = Steer.none
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def __call__(self):
        if not self.driving:
            self.both_motors.float()
            return
        # add power opposite side of steering direction
        left_power = self.direction * (self.speed + (30 if self.steer == Steer.right else 0))
        right_power = self.direction * (self.speed + (30 if self.steer == Steer.left else 0))
        self.left_motor.set_power(left_power)
        self.right_motor.set_power(right_power)
    def forward(self):
        self.driving = True
        self.direction = 1
        self.steer = Steer.none
    def reverse(self):
        self.driving = True
        self.direction = -1
        self.steer = Steer.none
    def left(self):
        self.steer = Steer.left
    def right(self):
        self.steer = Steer.right
    def stop(self):
        self.driving = False
    def faster(self):
        self.speed = min(self.speed + 10, 70)
    def slower(self):
        self.speed = max(self.speed - 10, 10)

    def get_steer(self):
        return self.reactor.variables['steer']
    def set_steer(self, steer):
        self.reactor.variables['steer'] = steer
    steer = property(get_steer, set_steer)
    def get_speed(self):
        return self.reactor.variables['speed']
    def set_speed(self, speed):
        self.reactor.variables['speed'] = speed
    speed = property(get_speed, set_speed)
