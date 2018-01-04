def bet(game, round, funds, game_record, round_record):
    if round == 0:
        return 0
    if round == 9:
        return funds[0]
    return max(0, round_record[-1][1] - 1)
