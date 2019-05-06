import datetime
import collections
import brickpictrlr
import robocore

DataPoint = collections.namedtuple('DataPoint', 'timestamp compass left_sound right_sound')

class ScanController(robocore.BaseController):
    REQUIREMENTS = {'twowheel', 'console', 'brick'}
    def __init__(self, core, left_sound_port, right_sound_port, compass_port):
        super().__init__(core)
        self.left_sound_port = left_sound_port
        self.right_sound_port = right_sound_port
        self.compass_port = compass_port
        self.data = []
        self.strategy = self.idle
    def __enter__(self):
        brick = self.core.controllers['brick']
        console = self.core.controllers['console']
        self.twowheel = self.core.controllers['twowheel']
        console.set_key('s', self.do_scan)
        console.set_key('i', self.do_idle)
        console.set_key('d', self.dump_data)
        self.left_sound = brick.new_sensor(brickpictrlr.SoundSensor, brick.PORT_2, name='leftsound')
        self.right_sound = brick.new_sensor(brickpictrlr.SoundSensor, brick.PORT_1, name='rightsound')
        self.compass = brick.new_sensor(brickpictrlr.CompassSensor, brick.PORT_4)
        return self
    def __call__(self):
        self.strategy()
    def idle(self):
        pass
    def scan(self):
        if not self.twowheel.driving:
            self.twowheel.speed = 10
            self.twowheel.forward()
            self.twowheel.left()
        point = DataPoint(
            timestamp = self.core.loop.time(),
            compass = self.compass(),
            left_sound = self.left_sound(),
            right_sound = self.right_sound(),
        )
        self.data.append(point)
        self.core.variables['data_len'] = len(self.data)
    def do_scan(self):
        self.strategy = self.scan
    def do_idle(self):
        self.strategy = self.idle
        self.twowheel.stop()
    def set_strategy(self, strategy):
        self.strategy = strategy
    def dump_data(self):
        size = 0
        now = datetime.datetime.now().strftime('%y%m%d-%H%M%S')
        with open('/tmp/data.%s.csv' % (now,), 'w') as handle:
            size += handle.write('timestamp,compass,left_sound,right_sound\n')
            for point in self.data:
                size += handle.write('%.1f,%d,%d,%d\n' % point)
        self.core.log("dumped %d points, %d bytes" % (len(self.data), size))
        self.data = []
        self.core.variables['data_len'] = len(self.data)
