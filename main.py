import cv2
import numpy as np
from PIL import Image
# import mss
# import win32gui #where we use it?
import pyautogui
import pygetwindow as gw
import keyboard
import time
from datetime import datetime
fps = 30
gisteresis_st=20
gisteresis_th=10
gisteresis_br=30
target_speed=60
amount_dif = gisteresis_st
size=0.05

class Steering:
    def steering_amount(v, amount_l, amount_r):
        if amount_l + amount_r == 0:
            return(0)
        else:
            turn = (amount_r - amount_l) * (v / 220) / (amount_r + amount_l)
            if turn > 100:
                turn = 100
            return(turn * 100)

class Movements:
    '''use move. method to: do some of this things:'''
    def __init__(self):
        self.pressed = {'w': True, 'a': False, 's': False, 'd': False}
        
    def gas(self):
        if(self.pressed['s']): 
            keyboard.release("s")
            self.pressed['s'] = False
        keyboard.press("w")
        self.pressed['w'] = True

    def brake(self):
        if(self.pressed['w']): 
            keyboard.release("w")
            self.pressed['w'] = False
        keyboard.press("s")
        self.pressed['s'] = True

    def roll(self):
        if(self.pressed['w']): 
            keyboard.release("w")
            self.pressed['w'] = False
        if(self.pressed['s']): 
            keyboard.release("s")
            self.pressed['s'] = False


    def left(self):
        if(self.pressed['d']): 
            keyboard.release("d")
            self.pressed['d'] = False
        keyboard.press("a")
        self.pressed['a'] = True

    def right(self):
        if(self.pressed['a']): 
            keyboard.release("a")
            self.pressed['a'] = False
        keyboard.press("d")
        self.pressed['d'] = True
    
    def straight(self):
        if(self.pressed['a']): 
            keyboard.release("a")
            self.pressed['a'] = False
        if(self.pressed['d']): 
            keyboard.release("d")
            self.pressed['d'] = False
    def realise_all(self):
        keyboard.release("w")
        keyboard.release("a")
        keyboard.release("s")
        keyboard.release("d")

    
        
move=Movements()


class Imcap: #Imcap == image capture
    '''Class for working with image capturing'''
    needed_time=int(datetime.now().microsecond +1e6/fps)%1e6
    # Returns a list of segment conditions:
    def get_speed_list(img):
        offset = 30
        segment_condition = []
        digit_condition = []

        img = cv2.resize(img, (92, 36))

        for i in range(3):
            segment_positions = [
                (int(7), int(13 + offset * i)),  # Top
                (int(11), int(4 + offset * i)),  # Top Left
                (int(11), int(22 + offset * i)),  # Top right
                (int(18), int(13 + offset * i)),  # Middle
                (int(26), int(4 + offset * i)),  # Bottom Left
                (int(26), int(22 + offset * i)),  # Bottom Right
                (int(30), int(13 + offset * i))  # Bottom
            ]
            for segment in segment_positions:
                segment_condition.append(img[segment])

            digit_condition.append(segment_condition)
            segment_condition = []

        return(digit_condition)

    # Converts speed_list to a number:
    def get_speed(speed_list):
        speed = [0,0,0]
        for i in range(3):
            if speed_list[i][0] == 255:
                if speed_list[i][3] == 255 :
                    speed[i] = 0
                if speed_list[i][2] == speed_list[i][5] == 0:
                    speed[i] = 1
                elif speed_list[i][3] == 0:
                    speed[i] = 4

            elif speed_list[i][0] == 0:
                if speed_list[i][3] == 255:
                    speed[i] = 0
                elif speed_list[i][2] == 255:
                    if speed_list[i][4] == 0:
                        speed[i] = 6
                    else:
                        speed[i] = 5
                elif speed_list[i][1] == 255:
                    if speed_list[i][4] == 0:
                        speed[i] = 2
                    else:
                        speed[i] = 3
                elif speed_list[i][1] == 0 == speed_list[i][2]:
                    if speed_list[i][4] == 0:
                        speed[i] = 8
                    else:
                        speed[i] = 9
                elif speed_list[i][2] == 0:
                    speed[i] = 7
        v = 100 * speed[0] + 10 * speed[1] + speed[2]
        return(v)
        
    # Splits the window for the further analysis of each part
    def get_rects(window):
        map_rect = (window.left + int(window.width * 0.055),
                window.top + int(window.height * 0.65),
                int(window.width * 0.21),
                int(window.height * 0.27))
        
        speed_rect = (window.left + int(window.width * 0.805),
                  window.top + int(window.height * 0.82),
                  int(window.width * 0.08),
                  int(window.height * 0.05))

        # return(map_rect, map_rect_l, map_rect_r, speed_rect)
        return(map_rect, speed_rect)
    
    def get_brightness_amount(map_frame, x, y):
        global size
        a = int(map_frame.shape[0] * size)

        map_frame_l = map_frame[y - a : y,
                                x - a : x]

        map_frame_r = map_frame[y - a : y,
                                x : x + a]

        amount_l = np.average(map_frame_l)
        amount_r = np.average(map_frame_r)
        return(map_frame_l, map_frame_r, amount_l, amount_r)
    
    def turning(amount_l, amount_r):
        delta = amount_l - amount_r #not used
        if delta**2 <= 10:
            return(Movements.gas)
        elif delta > 0:
            return(Movements.left)
        elif delta < 0:
            return(Movements.right)

    def limiter():
        global fps
        if(datetime.now().microsecond<Imcap.needed_time): time.sleep((Imcap.needed_time-datetime.now().microsecond)/1e6)
        Imcap.needed_time=int(datetime.now().microsecond +1e6/fps)%1e6

    def get_center(mask):
        for y in range(int(mask.shape[0] / 3), int(mask.shape[0] * 2 / 3)):
            for x in range(int(mask.shape[1] / 3), int(mask.shape[1] * 2 / 3)):
                if mask[y, x] > 100:
                    return(x, y)

# Blurring mask:
kernel = np.ones((20, 20), 'uint8')

time.sleep(5)
move.gas()
pad.update()
time.sleep(5)
move.roll()
pad.update()
time.sleep(5)

'''Этот кусочек кода делает скрин'''
window_name = "Need for Speed™ Most Wanted"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
window = gw.getWindowsWithTitle(window_name)[0]
window.activate()
time.sleep(10)
while True:
    #Imcap.limiter()
    window_rect = (window.left, window.top, window.width, window.height)

    # Breaking the window into segments:
    map_rect, speed_rect = Imcap.get_rects(window)[0:4]

    nfs_map = np.array(pyautogui.screenshot(region=map_rect))
    nfs_speed = np.array(pyautogui.screenshot(region=speed_rect))

    (thresh, nfs_speed) = cv2.threshold(nfs_speed, 50, 255, cv2.THRESH_BINARY)  # Darker speedometer pixels screening out
    nfs_speed = cv2.cvtColor(nfs_speed, cv2.COLOR_BGR2GRAY)


    nfs_map = cv2.cvtColor(nfs_map, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(nfs_map, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([101, 72, 40]), np.array([255, 255, 255]))
    center = Imcap.get_center(mask)

    frame_speed = np.array(nfs_speed)
    frame_map = np.array(nfs_map)
    
    speed_list = Imcap.get_speed_list(frame_speed)
    speed=Imcap.get_speed(speed_list)
    
    if center != None:
        x, y = center
        threshed_map = cv2.cvtColor(nfs_map, cv2.COLOR_BGR2GRAY)
        (thresh, threshed_map) = cv2.threshold(nfs_map, 150, 255, cv2.THRESH_BINARY)
        threshed_map = cv2.cvtColor(threshed_map, cv2.COLOR_BGR2GRAY)
        nfs_map_l, nfs_map_r, amount_l, amount_r = Imcap.get_brightness_amount(threshed_map, x, y)
        frame_map_l = np.array(nfs_map_l)
        frame_map_r = np.array(nfs_map_r)
        cv2.imshow("Left-side map", frame_map_l)
        cv2.imshow("Right-side map", frame_map_r)
        print(Steering.steering_amount(speed, amount_l, amount_r))
        move.turn(Steering.steering_amount(speed, amount_l, amount_r))
        if((amount_l-amount_dif) <= amount_r >= (amount_l + amount_dif)):
            move.gas()
            print("gas")
        elif((speed-target_speed)>gisteresis_br):
            #move.brake()
            pass
        elif(): move.roll()
        move.update()


    '''
    #steering control
    if(abs(amount_l-amount_r)<gisteresis_st):
        move.straight()
    elif(amount_r<amount_l):
        move.left()
    elif(amount_r>amount_l):
        move.right()
    #throttle control
    if((amount_l-amount_dif) <= amount_r >= (amount_l + amount_dif)):
        move.gas()
    elif((speed-target_speed)>gisteresis_br):
        move.brake()
    elif(): move.roll()
    '''  
    # eliif n_r2 - 10 <= n_l2 = > n_r2 + 10:
    #     nitro = 1
    # print(n_r, n_l, right, left, turn, nitro)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
move.realise_all()
