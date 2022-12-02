import cv2
import numpy as np
from PIL import Image
import mss
#import win32gui #where we use it?
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
window = gw.getWindowsWithTitle(window_name)[0]
window.activate()

while True:
    window_rect = (window.left, window.top, window.width, window.height)

    # Обрезает окно по миникарте:
    map_rect = (window.left + int(window.width * 0.055),
                window.top + int(window.height * 0.65),
                int(window.width * 0.21),
                int(window.height * 0.27))
    speed_rect = (window.left + int(window.width * 0.805),
                  window.top + int(window.height * 0.82),
                  int(window.width * 0.08),
                  int(window.height * 0.05))

    nfs_map = pyautogui.screenshot(region=map_rect)
    nfs_speed = pyautogui.screenshot(region=speed_rect)

    # erode_speed = cv2.erode(nfs_speed, kernel, iterations=1)  # сглаживание
    (thresh, nfs_speed) = cv2.threshold(nfs_speed, 50, 255, cv2.THRESH_BINARY)  # отсеивание пикселей
    nfs_speed = cv2.cvtColor(nfs_speed, cv2.COLOR_BGR2GRAY)

    frame_map = np.array(nfs_map)
    frame_speed = np.array(nfs_speed)

    cv2.imshow("Map", frame_map)
    cv2.imshow("Speed", frame_speed)
    print(frame_map.shape)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
