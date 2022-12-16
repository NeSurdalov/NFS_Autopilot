def steering_amount(v, amount_l, amount_r):
        if amount_l + amount_r == 0:
            return(0)
        else:
            turn = (amount_r - amount_l) * (v / 220)**2 / (amount_r + amount_l)
            if turn > 1:
                turn = 1
            return(turn * 100)
