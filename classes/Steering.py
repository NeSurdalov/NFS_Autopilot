def steering_amount(v, amount_l, amount_r):
    class Steering:
        def steering_amount(v, amount_l, amount_r):
            no_turn = 0
            if amount_l + amount_r == 0:
                return (0)
            else:
                turn = (amount_r - amount_l) * (
                        np.exp(v / 220 - 1) * ((amount_r - amount_l) ** 2 / (amount_r + amount_l) ** 2)) / (
                               amount_r + amount_l)
                if turn > 100:
                    turn = 100
                if v == 0 and amount_l == amount_r == 0:
                    turn = 0.2
                return (turn * 100)