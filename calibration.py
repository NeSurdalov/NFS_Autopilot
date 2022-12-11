import vgamepad as vg
import time
pad = vg.VX360Gamepad()
class move:
    '''use move. method to: do some of this things:'''
        
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
    '''select gas, wait for binding your key, next do the same with brake and right turn'''
time.sleep(5) 
move.gas()
pad.update()
time.sleep(0.5)
move.roll()
pad.update()
time.sleep(5)
move.brake()
pad.update()
time.sleep(0.5)
move.roll()
pad.update()
time.sleep(5)
move.turn(100)
pad.update()
time.sleep(0.5)
move.turn(0)
pad.update()
time.sleep(10)

