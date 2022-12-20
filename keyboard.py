import keyboard
from time import sleep
''' it is backup for old version of emulation steering'''
class movements:
    '''use move. method to: do some of this things:'''
    def __init__(self):
        self.w_pressed=False
        self.s_pressed=False
        self.a_pressed=False
        self.d_pressed=False

    def gas(self):
        if(self.s_pressed): 
            keyboard.release("s")
            self.s_pressed=False
        keyboard.press("w")
        self.w_pressed=True


    def brake(self):
        if(self.w_pressed): 
            keyboard.release("w")
            self.w_pressed=False
        keyboard.press("s")
        self.s_pressed=True

    def left(self):
        if(self.d_pressed): 
            keyboard.release("d")
            self.d_pressed=False
        keyboard.press("a")
        self.a_pressed=True

    def right(self):
        if(self.a_pressed): 
            keyboard.release("a")
            self.a_pressed=False
        keyboard.press("d")
        self.d_pressed=True
    
    def straight(self):
        if(self.a_pressed): 
            keyboard.release("a")
            self.a_pressed=False
        if(self.d_pressed): 
            keyboard.release("d")
            self.d_pressed=False
        
move=movements()
        
move=movements()
sleep(5)
move.right()
move.gas()
sleep(10)
move.brake()
move.left()
sleep(10)
