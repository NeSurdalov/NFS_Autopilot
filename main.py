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
gisteresis_st=15
gisteresis_th=5
gisteresis_br=30
target_speed=60
class Movements:
    '''use move. method to: do some of this things:'''
    def __init__(self):
        self.pressed = {'w': True, 'a': False, 's': False, 'd': False}
        '''
        self.w_pressed=False
        self.s_pressed=False
        self.a_pressed=False
        self.d_pressed=False
        '''
        
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

    
        
move=Movements()


class Imcap: #Imcap == image capture
    '''Class for working with image capturing'''
    prev_time=datetime.now().microsecond
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
                    speed[i] = 7
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
        v = 100 * speed[0] + 10 * speed[1] + speed[2]
        return(v)
        
    # Breaks the window rect into different rects for the further processing of the ones
    def get_rects(window):
        map_rect = (window.left + int(window.width * 0.055),
                window.top + int(window.height * 0.65),
                int(window.width * 0.21),
                int(window.height * 0.27))
        
        '''
        map_rect_l = (map_rect[0],
                 map_rect[1],
                 int(map_rect[2] * 0.5),
                 int(map_rect[3] * 0.5))

        map_rect_r = (map_rect[0] + map_rect[2] * 0.5,
                 map_rect[1],
                 int(map_rect[2] * 0.5),
                 int(map_rect[3] * 0.5))    

        '''
        speed_rect = (window.left + int(window.width * 0.805),
                  window.top + int(window.height * 0.82),
                  int(window.width * 0.08),
                  int(window.height * 0.05))

        # return(map_rect, map_rect_l, map_rect_r, speed_rect)
        return(map_rect, speed_rect)

    
    def get_brightness_amount(map_frame):
        map_shape = map_frame.shape
        map_frame = map_frame[0:int(map_shape[0]), int(map_shape[1] * 0.015):int(map_shape[1])]
        map_shape = map_frame.shape

        map_frame_l = map_frame[int(map_shape[0] / 2 - map_shape[0] / 5) : int(map_shape[0] / 2),
                                int(map_shape[0] / 2 - map_shape[0] / 5) : int(map_shape[0] / 2)]

        map_frame_r = map_frame[int(map_shape[0] / 2 - map_shape[0] / 5) : int(map_shape[0] / 2),
                                int(map_shape[0] / 2) : int(map_shape[0] / 2 + map_shape[0] / 5)]

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
        if(datetime.now().microsecond<(Imcap.prev_time+1e6/fps)): time.sleep((Imcap.prev_time+1e6/fps-datetime.now().microsecond)/1e6)
        Imcap.prev_time=datetime.now().microsecond  #FIXME freezes every 3 seconds

# Blurring mask:
kernel = np.ones((20, 20), 'uint8')

'''Этот кусочек кода делает скрин'''
window_name = "Need for Speed™ Most Wanted"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
window = gw.getWindowsWithTitle(window_name)[0]
window.activate()

while True:
    Imcap.limiter()
    window_rect = (window.left, window.top, window.width, window.height)

    # Breaking the window into segments:
    # map_rect, map_rect_l, map_rect_r, speed_rect = Imcap.get_rects(window)[0:4]
    map_rect, speed_rect = Imcap.get_rects(window)[0:4]

    nfs_map = np.array(pyautogui.screenshot(region=map_rect))
    nfs_speed = np.array(pyautogui.screenshot(region=speed_rect))

    # nfs_map_l = np.array(pyautogui.screenshot(region=map_rect_l))
    # nfs_map_r = np.array(pyautogui.screenshot(region=map_rect_r))

    (thresh, nfs_speed) = cv2.threshold(nfs_speed, 50, 255, cv2.THRESH_BINARY)  # Darker speedometer pixels screening out
    nfs_speed = cv2.cvtColor(nfs_speed, cv2.COLOR_BGR2GRAY)

    nfs_map = cv2.cvtColor(nfs_map, cv2.COLOR_BGR2GRAY)
    # (thresh, nfs_map) = cv2.threshold(nfs_map, 180, 255, cv2.THRESH_BINARY)  # Darker map pixels screening out
    # nfs_map = cv2.morphologyEx(nfs_map, cv2.MORPH_CLOSE, kernel)

    nfs_map_l, nfs_map_r, amount_l, amount_r = Imcap.get_brightness_amount(nfs_map)

    frame_speed = np.array(nfs_speed)
    frame_map = np.array(nfs_map)
    frame_map_l = np.array(nfs_map_l)
    frame_map_r = np.array(nfs_map_r)

    cv2.imshow("Map", frame_map)
    cv2.imshow("Speed", frame_speed)

    cv2.imshow("Left-side map", frame_map_l)
    cv2.imshow("Right-side map", frame_map_r)

    speed_list = Imcap.get_speed_list(frame_speed)
    speed=Imcap.get_speed(speed_list)
    print(speed)
    print(amount_l, amount_r)
    #steering control
    '''if(abs(amount_l-amount_r)<gisteresis_st):
        move.straight()
    elif(amount_r>amount_l):
        move.left()
    elif(amount_r<amount_l):
        move.right()
    #throttle control
    if((target_speed-speed)>gisteresis_th):
        move.gas()
    elif((speed-target_speed)>gisteresis_br):
        move.brake()
    elif(): move.roll()'''
    

    print()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('images/speed_screenshot.jpg', nfs_speed)
        cv2.imwrite('images/map_l.jpg', nfs_map_l)
        cv2.imwrite('images/map_r.jpg', nfs_map_r)
        cv2.imwrite('images/map.jpg', nfs_map)
        break


def color_pixel_count(img_r,img_l):
    '''
    Count number of pixels in diferent colors
    :param map_rect_r: right side of minimap
    :param map_rect_l: left side of mininap
    :return: n_l and n_r
    '''

    for pixel in map_rect_r.getdata():
        if pixel == (250,250,250) :
            n_r += 1

    for pixel in map_rect_l.getdata():
        if pixel == (250,250,250) :
            n_l += 1
