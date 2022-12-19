import numpy as np

def steering_amount(v, amount_l, amount_r):
    turn = (amount_r - amount_l) * (
                np.exp(v / 220 - 1) * ((amount_r - amount_l) ** 2 / (amount_r + amount_l) ** 2)) / (
                        amount_r + amount_l)
    print(turn, type(turn))
    if np.isnan(turn):
        turn = 0
    elif turn > 1:
        turn = 1
    return (turn * 100)