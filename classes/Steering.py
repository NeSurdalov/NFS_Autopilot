class Steering:
    def steering_amount(v, amount_l, amount_r):
        turn_list1 = 0
        # no_turn = 0
        if amount_l + amount_r == 0:
            return(0)
        else:
            turn = (amount_r - amount_l) * (np.exp(v/220-1)*((amount_r - amount_l)**2/(amount_r + amount_l)**2)) / (amount_r + amount_l)
            turn_list1 += turn
            # turn_list1.append(turn)
            # turn_list2 = turn_list1[:5]
            # turn_lenghts = len(turn_list2)
            # for i in range( turn_lenghts , -1) :
            #     while turn_list2[i] != 0 :
            #         no_turn =+1
            # if no_turn >= 4 and v == 0:
            #     turn = turn_list2[turn_lenghts-no_turn-2]
            # if turn > 100:
            #     turn = 100
            # print(turn * 100)
            # print(turn_list2[turn_lenghts-no_turn-2],"last turn")
            if v==0 :
                turn = turn_list1
            print(turn_list1,"turn")