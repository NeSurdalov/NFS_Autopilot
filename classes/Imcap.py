'''Class for working with image capturing'''

# Returns a list of segment conditions:
from datetime import datetime
import cv2
import numpy as np

fps = 30
size = 0.1
needed_time=int(datetime.now().microsecond +1e6 / fps) % 1e6

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
    # global size
    a = int(map_frame.shape[0] * size)

    map_frame_l = map_frame[y - a : y,
                            x - a : x]

    map_frame_r = map_frame[y - a : y,
                            x : x + a]

    amount_l = np.average(map_frame_l)
    amount_r = np.average(map_frame_r)
    return(map_frame_l, map_frame_r, amount_l, amount_r)
    
def get_center(mask):
    for y in range(int(mask.shape[0] / 3), int(mask.shape[0] * 2 / 3)):
        for x in range(int(mask.shape[1] / 3), int(mask.shape[1] * 2 / 3)):
            if mask[y, x] > 100:
                return(x, y)
