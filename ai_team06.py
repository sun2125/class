def bet(game, round, funds, game_record, round_record):
    import random
    import numpy as np
    if round == 9: 
        return funds[0]
    # if round == 9:
    #     return 0
    ran = random.randint(8,11)
    ran /= 10

    ran2 = random.randint(10,11)
    ran2 /= 10

    if game < 5:
        if round <= 4:
            return int(1000*ran)
        elif funds[0] > funds[1]:
            re = int(1000*ran2)
        else:
            re = int(800*ran)
        if re < funds[0]:
            if re < 0: re *= -1
            return re
        else:
            return 0
        #     return int(1000*ran2)
        # else:
        #     return int(800*ran)

    else:
        if round <= 5:
            return int(1000*ran)
        else:
            data = game_record[game-20:]
            data2 = [gr[round][1] for gr in data]
            d = np.median(data2)
            x = d-100
            if x<0: x*=-1
            return int(x)
