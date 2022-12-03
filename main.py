import cv2
import numpy as np
from PIL import Image
# import mss
# import win32gui #where we use it?
import pyautogui
import pygetwindow as gw
import keyboard

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


class imcap: #imcap=image capture
    '''Class for working with image capturing'''
    
    def get_speed_list(img):
        offset = 30
        segment_condition = []
        digit_condition = []

        cv2.resize(img, (92, 36))
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

    def get_speed(speed_list):
    for i in range(3)
        if speed_list[i][0] == 255 :
            if speed_list[i][3]==speed_list[i][6]==0 : 
                speed[i] = 1
            elif speed_list[i][3]==0: 
                speed[i] = 4
        elif speed_list[i][0] == 0:
            if speed_list[i][3] == 255 :
                speed[i] = 7
            elif speed_list[i][2] == 255:
                if speed_list[i][4] == 0 :
                    speed[i] = 6
                else:
                    speed[i] = 5
            elif speed_list[i][1] == 255 :
                if speed_list[i][4] == 0 :
                    speed[i] = 2
                else : 
                    speed[i] = 3
            elif speed_list[i][1] == 0 == speed_list[i][2] :
                if speed_list[i][4] == 0 :
                    speed[i] = 8
                else : 
                    speed[i] = 9
    v = 100*speed[0] + 10*speed[1] + speed[2]


# маска для сглаживания входящей картинки:
kernel = np.ones((5, 5), 'uint8')

'''Этот кусочек кода делает скрин'''
window_name = "Need for Speed™ Most Wanted"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 30.0
window = gw.getWindowsWithTitle(window_name)[0]
window.activate()

while True:
    window_rect = (window.left, window.top, window.width, window.height)

    # Обрезает окно по миникарте:
    map_rect_r = (window.left + int(window.width * 0.075),
                window.top + int(window.height * 0.65),
                int(window.width * 0.21),
                int(window.height * 0.27))
    map_rect_l = (window.left + int(window.width * 0.025),
                 window.top + int(window.height * 0.65),
                 int(window.width * 0.05),
                 int(window.height * 0.05))
    speed_rect = (window.left + int(window.width * 0.805),
                  window.top + int(window.height * 0.82),
                  int(window.width * 0.08),
                  int(window.height * 0.05))

    nfs_map = np.array(pyautogui.screenshot(region=map_rect))
    nfs_speed = np.array(pyautogui.screenshot(region=speed_rect))

    # erode_speed = cv2.erode(nfs_speed, kernel, iterations=1)  # сглаживание
    (thresh, nfs_speed) = cv2.threshold(nfs_speed, 50, 255, cv2.THRESH_BINARY)  # отсеивание пикселей
    nfs_speed = cv2.cvtColor(nfs_speed, cv2.COLOR_BGR2GRAY)

    frame_map = np.array(nfs_map)
    frame_speed = np.array(nfs_speed)

    cv2.imshow("Map", frame_map)
    cv2.imshow("Speed", frame_speed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('images/speed_screenshot.jpg', nfs_speed)
        print(imcap.get_speed_list(nfs_speed))
        break


def color_pixel_count(img_r,img_l):
    '''
    Count number of pixels in diferent colors
    :param map_rect_r: right side of minimap
    :param map_rect_l: left sude of mininap
    :return: n_l and n_r
    '''
    # from PIL import *

    for pixel in map_rect_r.getdata():
        if pixel is (250,250,250) :
            n_r += 1

    for pixel in map_rect_l.getdata():
        if pixel is (250,250,250) :
            n_l += 1