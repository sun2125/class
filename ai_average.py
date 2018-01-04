def bet(game, round, funds, game_record, round_record):
    if game < 1:
        return 1000
    if round == 9:
        return funds[0]
    return sum(gr[round][1] for gr in game_record) // game
