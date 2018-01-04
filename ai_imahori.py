def bet(game, round, funds, game_record, round_record):
    import random

    if round == 9: return funds[0]

    para = 0.9 + 0.1 * random.random()

    if round == 0:  
        if game < 5:  return 1000
        else:  
            data = game_record[game-5:]
            data2 = [gr[0][1] for gr in data]
            median = sorted(data2)[len(data2) // 2]
            return min(int(4000*para), int(median * para))

    flag = random.randint(0, 3)

    if flag == 0:
        if game < 5:  
            return min(funds[0], 1000) 
        else:
            data = game_record[game-5:]
            data2 = [gr[round][1] for gr in data]
            median = sorted(data2)[len(data2) // 2]
            return min(funds[0], int(median * para))
    elif flag == 1: 
        if funds[0] > funds[1]:
            return (funds[0] - ((9 - round) * funds[1] // (10 - round)))
        return min(funds[0], (2 - para) * funds[0] // (10 - round))
    else: 
        if funds[0] > funds[1]:
            return int(para * (funds[1] // (10 - round)))
        return int(para * (funds[0] // (10 - round)))
