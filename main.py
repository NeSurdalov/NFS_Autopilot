import cv2
import numpy as np
from PIL import Image
# import mss
# import win32gui #where we use it?
import pyautogui
import pygetwindow as gw

class imcap: #imcap=image capture
    '''Class for working with image capturing'''
    pass
    
    

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
    print(frame_map.shape)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # cv2.imshow('speed_creenshot', nfs_speed)
        break

def color_pixel_count(map_rect_r,map_rect_l):
    '''
    Count number of pixels in diferent colors
    :param map_rect_r: right side of minimap
    :param map_rect_l: left sude of mininap
    :return: n_l and n_r
    '''
    from PIL import *

    for pixel in map_rect_r.getdata():
        if pixel is (250,250,250) :
            n_r += 1

    for pixel in map_rect_l.getdata():
        if pixel is (250,250,250) :
            n_l += 1