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
import classes.Steering as Steering
from classes.Move import *
import classes.Imcap as Imcap

gisteresis_st=5
gisteresis_th=10
gisteresis_br=30
target_speed=60
amount_dif = gisteresis_st
size=0.05
kernel = np.ones((20, 20), 'uint8')

gas()
pad.update()
roll()
pad.update()
time.sleep(5)

# Taking a screenshot:
window_name = "Need for Speed™ Most Wanted"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
window = gw.getWindowsWithTitle(window_name)[0]
if window != []:
    try:
        window.activate()
    except:
        window.maximize()
while True:
    window_rect = (window.left, window.top, window.width, window.height)

    # Breaking the window into segments:
    map_rect, speed_rect = Imcap.get_rects(window)[0:4]

    # Taking a screenshot of a certain segment:
    nfs_map = np.array(pyautogui.screenshot(region=map_rect))
    nfs_speed = np.array(pyautogui.screenshot(region=speed_rect))

    # Screening out the darker speedometer pixels:
    (thresh, nfs_speed) = cv2.threshold(nfs_speed, 50, 255, cv2.THRESH_BINARY)
    nfs_speed = cv2.cvtColor(nfs_speed, cv2.COLOR_BGR2GRAY)

    # Getting the coordinates of the map center and centering the map rect:
    nfs_map = cv2.cvtColor(nfs_map, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(nfs_map, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([101, 72, 40]), np.array([255, 255, 255]))
    center = Imcap.get_center(mask)
    
    # Getting the speed amount: 
    speed_list = Imcap.get_speed_list(nfs_speed)
    speed=Imcap.get_speed(speed_list)
    
    # If the game window is not opened, 'center' will be of value 'None' which breakes the script,
    # so we take all the lines that use 'center' variable and put them into an if statement:
    if center != None:
        x, y = center

        # Screening out the darker map pixels:
        threshed_map = cv2.cvtColor(nfs_map, cv2.COLOR_BGR2GRAY)
        (thresh, threshed_map) = cv2.threshold(nfs_map, 150, 255, cv2.THRESH_BINARY)
        threshed_map = cv2.cvtColor(threshed_map, cv2.COLOR_BGR2GRAY)

        # Getting two bites of the map on the top-left side of
        nfs_map_l, nfs_map_r, amount_l, amount_r = Imcap.get_brightness_amount(threshed_map, x, y)
        map_l = np.array(nfs_map_l)
        map_r = np.array(nfs_map_r)
        cv2.imshow("Left-side map", map_l)
        cv2.imshow("Right-side map", map_r)
        print(Steering.steering_amount(speed, amount_l, amount_r))
        turn(Steering.steering_amount(speed, amount_l, amount_r))
        if((amount_l-amount_dif) <= amount_r >= (amount_l + amount_dif)):
            gas()
            print("gas")
        elif((speed-target_speed)>gisteresis_br):
            #Move.brake()
            pass
        elif(): roll()
        update()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
release_all()
