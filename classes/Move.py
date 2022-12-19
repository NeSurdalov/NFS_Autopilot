'''use Move. method to: do some of this things:'''

import vgamepad as vg
pad = vg.VX360Gamepad()

def gas(value=100):
    gain=int(value/100*255) 
    pad.left_trigger(0)
    pad.right_trigger(gain)

def brake(value=100):
    gain=int(value/100*255) 
    pad.right_trigger(0)
    pad.left_trigger(gain)

def roll():
    pad.right_trigger(0)
    pad.left_trigger(0)


def turn(value=100):
    gain=int(value/100*32767)
    pad.left_joystick(x_value=gain,y_value=0)
def update():
    pad.update()
def release_all():
    pad.reset()
    pad.update()
