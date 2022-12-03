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


class imcap: #imcap == image capture
    '''Class for working with image capturing'''
    
    # Returns a list of segment conditions:
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

    # Converts speed_list to a number:
    def get_speed(speed_list):
        speed = []
        
        v = 100*speed[0] + 10*speed[1] + speed[2]
        return(v)

    # Breaks the window rect to 
    def get_rects(window):
        map_rect = (window.left + int(window.width * 0.055),
                window.top + int(window.height * 0.65),
                int(window.width * 0.21),
                int(window.height * 0.27))

        map_rect_l = (map_rect[0],
                 map_rect[1],
                 int(map_rect[2] * 0.5),
                 int(map_rect[3] * 0.5))

        map_rect_r = (map_rect[0],
                 map_rect[1] + map_rect[2] * 0.5,
                 int(map_rect[2] * 0.5),
                 int(map_rect[3] * 0.5))    

        speed_rect = (window.left + int(window.width * 0.805),
                  window.top + int(window.height * 0.82),
                  int(window.width * 0.08),
                  int(window.height * 0.05))

        return(map_rect, map_rect_l, map_rect_r, speed_rect)




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
    map_rect, map_rect_l, map_rect_r, speed_rect = imcap.get_rects(window)[0:4]

    nfs_map = np.array(pyautogui.screenshot(region=map_rect))
    nfs_speed = np.array(pyautogui.screenshot(region=speed_rect))
    nfs_map_l = np.array(pyautogui.screenshot(region=map_rect_l))
    nfs_map_r = np.array(pyautogui.screenshot(region=map_rect_r))

    # erode_speed = cv2.erode(nfs_speed, kernel, iterations=1)  # сглаживание
    (thresh, nfs_speed) = cv2.threshold(nfs_speed, 50, 255, cv2.THRESH_BINARY)  # отсеивание пикселей
    nfs_speed = cv2.cvtColor(nfs_speed, cv2.COLOR_BGR2GRAY)

    frame_map = np.array(nfs_map)
    frame_speed = np.array(nfs_speed)

    cv2.imshow("Map", frame_map)
    cv2.imshow("Speed", frame_speed)

    speed_list = imcap.get_speed_list(frame_speed)
    print(imcap.get_speed(speed_list))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('images/speed_screenshot.jpg', nfs_speed)
        cv2.imwrite('images/map_l.jpg', nfs_map_l)
        cv2.imwrite('images/map_r.jpg', nfs_map_r)
        cv2.imwrite('images/map.jpg', nfs_map)
        speed_list = imcap.get_speed_list(nfs_speed)
        print(imcap.get_speed(speed_list))
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
        if pixel == (250,250,250) :
            n_r += 1

    for pixel in map_rect_l.getdata():
        if pixel == (250,250,250) :
            n_l += 1
