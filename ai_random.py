def bet(game, round, funds, game_record, round_record):
    import random
    return random.randint(0, funds[0]) if round < 9 else funds[0]
