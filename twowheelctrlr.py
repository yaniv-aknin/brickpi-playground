import curses
import enum

class Steer(enum.Enum):
    left = 1
    none = 2
    right = 3

class TwoWheelController(object):
    def __init__(self, core, left_port, right_port):
        if {'console', 'brick'} & set(core.controllers) != {'console', 'brick'}:
            raise RuntimeError('need console and brick controllers')
        self.core = core
        self.left_port = left_port
        self.right_port = right_port
    def __enter__(self):
        brick = self.core.controllers['brick']
        console = self.core.controllers['console']
        self.left_motor = brick.new_motor(self.left_port, 'left')
        self.right_motor = brick.new_motor(self.right_port, 'right')
        self.both_motors = brick.new_motor_set('both', self.left_motor, self.right_motor)
        console.set_key(curses.KEY_UP, self.forward)
        console.set_key(curses.KEY_DOWN, self.reverse)
        console.set_key(curses.KEY_LEFT, self.left)
        console.set_key(curses.KEY_RIGHT, self.right)
        console.set_key(' ', self.stop)
        console.set_key('+', self.faster)
        console.set_key('-', self.slower)
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
        return self.core.variables['steer']
    def set_steer(self, steer):
        self.core.variables['steer'] = steer
    steer = property(get_steer, set_steer)
    def get_speed(self):
        return self.core.variables['speed']
    def set_speed(self, speed):
        self.core.variables['speed'] = speed
    speed = property(get_speed, set_speed)
