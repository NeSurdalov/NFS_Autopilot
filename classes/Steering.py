def steering_amount(v, amount_l, amount_r):
    class Steering:
        def steering_amount(v, amount_l, amount_r):
            no_turn = 0
            if amount_l + amount_r == 0:
                return (0)
            else:
                turn = (amount_r - amount_l) * ((v) ** 2 / 220) / (amount_r + amount_l)
                turn_list.append(turn)
                turn_lenghts = len(turn_list)
                for i in range(turn_lenghts, -1):
                    while turn_list[i] == 0:
                        no_turn = +1
                if no_turn >= 4 and v == 0:
                    turn = turn_list[turn_lenghts - no_turn]
                if turn > 100:
                    turn = 100
                return (turn * 100)