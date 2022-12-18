import cv2
import numpy as np
from PIL import Image
# import mss
# import win32gui #where we use it?
import pyautogui
import pygetwindow as gw
import keyboard
from time import time
from datetime import datetime
import classes.Steering as Steering
from classes.Move import *
import classes.Imcap as Imcap
from classes.WindowCapture import WindowCapture

gisteresis_st=50
gisteresis_th=10
gisteresis_br=30
target_speed=60
amount_dif = gisteresis_st
size=0.05
kernel = np.ones((20, 20), 'uint8')

gas()
pad.update()
# time.sleep(5)
roll()
pad.update()
# time.sleep(5)

'''Этот кусочек кода делает скрин'''
window_name = "Need for Speed™ Most Wanted"
# fourcc = cv2.VideoWriter_fourcc(*"XVID")
window = gw.getWindowsWithTitle(window_name)[0]

wincap = WindowCapture(window_name)
loop_time = time()

if window != []:
    try:
        window.activate()
    except:
        window.maximize()
while True:
    #Imcap.limiter()
    l, t, w, h = (window.left, window.top, wincap.w, wincap.h)
    window_rect = (l, t, w, h)

    # Breaking the window into segments:
    screenshot = wincap.get_screenshot()

    map_rect, speed_rect = Imcap.get_rects(l, t, w, h)[0:4]

    nfs_map = screenshot[map_rect[0] : map_rect[0] + map_rect[2], map_rect[1] : map_rect[1] + map_rect[3]]
    nfs_speed = screenshot[speed_rect[0] : speed_rect[0] + speed_rect[2], speed_rect[1] : speed_rect[1] + speed_rect[3]]
    
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
        nfs_map_l, nfs_map_r, amount_l, amount_r, amount_fl, amount_fr = Imcap.get_brightness_amount(threshed_map, x, y)
        frame_map_l = np.array(nfs_map_l)
        frame_map_r = np.array(nfs_map_r)
        cv2.imshow("Left-side map", frame_map_l)
        cv2.imshow("Right-side map", frame_map_r)
        turn(Steering.steering_amount(speed, amount_l, amount_r))
        print(abs(amount_fl - amount_fr))
        print(gisteresis_st / (speed / 220 + 1))
        if(abs((amount_fl - amount_fr)) <= gisteresis_st / (speed + 1)):
            gas()
        elif(abs((amount_fl - amount_fr)) >= gisteresis_br / (speed / 220 + 1) and speed >= 30):
            brake()
        elif(): roll()
        update()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('images/speed_screenshot.jpg', nfs_speed)
        break
cv2.destroyAllWindows()
release_all()
