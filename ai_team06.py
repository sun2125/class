def bet(game, round, funds, game_record, round_record):
    import random
    import numpy as np

    def median_check(game, round, s):
        data = game_record[game-5:]
        data2 = [gr[round][s] for gr in data]
        d = np.median(data2)
        cnt = 0
        mc = game_record[game-1][round][s] - d
        if abs(mc) < 50:
            cnt += 1
        if cnt >= 6:
            return True
        else:
            return False

    def average_check(game, round):
        g = 0
        for i in range(10):
            for j in range(game-1):
                g += game_record[j][i][0]
            g  = g // (game-1)
            if (g - game_record[game-2][round][1]) < 50:
                return True
            else:
                return False


    

    if round == 9: 
        return funds[0]

    ran = random.randint(7,11)
    ran /= 10

    ran2 = random.randint(10,11)
    ran2 /= 10

    ran3 = random.randint(5,15)
    ran3 /= 10

    a = 100

    if game < 5:

        if round < 4:
            return int(1000*ran)
        else:
            if funds[0] > funds[1]:
                re = int(1000*ran)
            else:
                re = int(800*ran)
            if re < funds[0]:
                if re < 0:
                    re *= -1
                return re
            else:
                return funds[0] // (9-round)
        #     return int(1000*ran2)
        # else:
        #     return int(800*ran)

    else:
        flag = average_check(game,round)
        if median_check(game, round, 1) == True and flag == False:
            if funds[0] > 1000 * (9-round):
                re == 1000*ran
            else:
                re == 800*ran
            if re > funds[0]:
                return funds[0] // (9-round)
            else:
                return re
        elif flag == True:
            data = game_record[game-5:]
            data2 = [gr[round][1] for gr in data]
            d = np.median(data2)
            x = d-(a*ran)
            if x<0: x*=-1
            if x > funds[0]:
                return funds[0] // (9-round)
            else:
                return int(x)
        else:
            data = game_record[game-5:]
            data2 = [gr[round][1] for gr in data]
            d = np.median(data2)
            cnt = 0
            for i in range(10):
                if game_record[game-1][0] > game_record[game-1][1]: cnt+=1
                if a > 0:
                    if cnt<=5:
                        a += 50
                    else:
                        a -= 50
                else:
                    a += 0
            x = d-(a*ran3)
            if x<0: x*=-1
            if x > funds[0]:
                return funds[0] // (9-round)
            elif x < 800:
                re = 800 * ran
                if re > funds[0]:
                    return funds[0] // (9-round)
                else:
                    return re
            else:
                return int(x)


