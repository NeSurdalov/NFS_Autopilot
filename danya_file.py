import cv2
import numpy as np
'''
from PIL import Image
import mss
import win32gui
import pyautogui
'''

# маска для сглаживания входящей картинки:
kernel = np.ones((5, 5), 'uint8')


def get_speed(img):
    h, w = img.shape[0:2]
    offset = 21
    segment_condition = []
    digit_condition = []
    digits = 3


    '''
    segment_positions = [
        (int(h * 0.12), int(w * 0.85)),     # Top
        (int(h * 0.28), int(w * 0.76)),     # Top Left
        (int(h * 0.28), int(w * 0.95)),     # Top right
        (int(h * 0.44), int(w * 0.85)),     # Middle
        (int(h * 0.6), int(w * 0.76)),      # Bottom Left
        (int(h * 0.6), int(w * 0.95)),      # Bottom Right
        (int(h * 0.78), int(w * 0.85))      # Bottom
    ]
    '''

    for i in range(digits):
        segment_positions = [
            (int(h * 0.12), int(w * 0.19 + offset * i)),  # Top
            (int(h * 0.28), int(w * 0.10 + offset * i)),  # Top Left
            (int(h * 0.28), int(w * 0.29 + offset * i)),  # Top right
            (int(h * 0.44), int(w * 0.19 + offset * i)),  # Middle
            (int(h * 0.6), int(w * 0.10 + offset * i)),  # Bottom Left
            (int(h * 0.6), int(w * 0.29 + offset * i)),  # Bottom Right
            (int(h * 0.78), int(w * 0.19 + offset * i))  # Bottom
        ]

        for segment in segment_positions:
            segment_condition.append(img[segment])

        digit_condition.append(segment_condition)
        segment_condition = []

    return digit_condition


def speed_determination(V, n_r, n_l, n_r2, n_l2):
    '''
       Получает на вход количества пикселей на разных частях экрана и исходя из этого понимает
    какие кнопки и сколько стоит нажимать
    dx-ширина области с которой каретка будет считывать значения
    dv-что-то типо норированного изменения скорости , по-типу нажатия кнопки вправо на протяжении 20 тиков
    dt-например 100 тиков
    :param V:
    :param n_r: Number of black pixels on right side
    :param n_l: Number of black pixels on left side
    :param n_r2: Number of black pixels on riht side on bigger area
    :param n_l2: Number of black pixels on left side on bigger area
    :return: turn - amount of pressing buttons
            nitro - nitro button
            right
            left
    '''

    r = 100 * dv
"""
Рассчитывает скорости вправо и влево
"""
    v_r = (n_r/(n_l+n_r))*np.exp(v*dt/dx)*dv
    v_l = (n_l/(n_l+n_r))*np.exp(v*dt/dx)*dv
if v_r => v_l :
    turn = v_r
    right = 1
    left = 0
else :
    turn = v_l
    left = 1
    right = 1

if v_l - rdv <= v_r = > v_l + rdv:
    v_r = v_l = 0

""" Начинает разгоняться """

if n_r - 10 <= n_l = > n_r + 10:
    v_s += 10 * dv

if n_r2 - 10 <= n_l2 = > n_r2 + 10:
    nitro = 1


while True:
    window_rect = (120, 650, 220, 220)  # область работыOpenCV
    # img = pyautogui.screenshot(region=window_rect)  # CV делает скриншот своей области
    img = cv2.imread('images/speed image.jpg')
    img = np.array(img)  # конвертация скриншота в список
    img = cv2.resize(img, (400, 200))
    # erode_img = cv2.erode(img, kernel, iterations=1)  # сглаживание
    (thresh, img) = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)  # отсеивание пикселей
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Output', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(get_speed(img))
        break
