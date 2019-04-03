import brickpi3
import atexit

def GetBrickHandle():
    brick = brickpi3.BrickPi3()
    brick.reset_all()
    atexit.register(brick.reset_all)
    return brick


