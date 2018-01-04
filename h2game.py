def setup():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        'filename',
        nargs=2,
        type=str,
        help='filename',
        metavar='FILENAME'
    )
    parser.add_argument(
        '-c',
        dest='game',
        default=1,
        type=int,
        help='number of games',
        metavar='N'
    )
    parser.add_argument(
        '--dumps',
        dest='dumps',
        action='store_true',
        help='log to images (default = false)',
    )
    parser.add_argument(
        '--quiet', '-q',
        dest='quiet',
        action='store_true',
        help='messages on/off (default = on)',
    )

    params = parser.parse_args().__dict__

    filename = params.get('filename', [])
    del params['filename']

    import re
    ai1, ai2 = [re.sub(r'.py$', '', fn).replace('/', '.') for fn in filename]

    params.update({'ai1': ai1, 'ai2': ai2})

    return params

def chrono(func):
    from datetime import datetime
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.today()

        result = func(*args, **kwargs)

        end = datetime.today()

        print("elapsed:", end - start)

        return result

    return wrapper

class H2Game(object):
    class Player(object):
        def __init__(self, module_name, *args, **kwargs):
            import importlib
            self.name = module_name
            self.module = importlib.import_module(module_name)

        # @chrono
        def bet(self, game, round, funds, game_record, round_record):
            return self.module.bet(game = game, round = round, funds = funds, 
                                   game_record = game_record,
                                   round_record = round_record)

    def __init__(self, ai1, ai2, game, **kwargs):
        self.player1 = self.Player(ai1)
        self.player2 = self.Player(ai2)
        self.game = game
        self.dumps = kwargs['dumps']

        import os
        import sys

        self.stdout = sys.stdout
        if kwargs['quiet']:
            try:
                self.stdout = open(os.devnull, 'w')
            except:
                pass

    def play_the_game(self):
        def handle(result, player, *args):
            result.value = player.bet(*args)

        from collections import deque

        win_record = ""
        game_record = deque()

        for g in range(self.game):
            print("game %d:" % g)
            round_record = deque()
            win1 = win2 = 0

            for r in range(10):
                print("  round %d:" % r)

                funds1 = 10000 - sum(rr[0] for rr in round_record)
                funds2 = 10000 - sum(rr[1] for rr in round_record)

                bet1 = self.player1.bet(g, r, (funds1, funds2),
                                        tuple(game_record), tuple(round_record))
                bet2 = self.player2.bet(g, r, (funds2, funds1),
                                        tuple([[(b, a) for a, b in record] for record in game_record]),
                                        tuple([(b, a) for a, b in round_record]))

                round_record.append((bet1, bet2))

                print("    judge: %d vs %d" % (bet1, bet2))

                win1 += bet1 * (bet1 <= bet2) + bet2 * (bet1 < bet2)
                win2 += bet1 * (bet1 > bet2) + bet2 * (bet1 >= bet2)

                print("    current score: %d vs %d" % (win1, win2))
                print("    remain funds: %d, %d" % (10000 - sum(rr[0] for rr in round_record),
                                                    10000 - sum(rr[1] for rr in round_record)))

            valid1 = sum(rr[0] for rr in round_record) == 10000 and all(0 <= rr[0] for rr in round_record)
            valid2 = sum(rr[1] for rr in round_record) == 10000 and all(0 <= rr[1] for rr in round_record)
            if not (valid1 or valid2):
                raise Exception("error: both player are violation of regulation.")

            elif not valid1:
                raise Exception("error: %s is violation of regulation." % self.player1.name)

            elif not valid2:
                raise Exception("error: %s is violation of regulation." % self.player2.name)

            print("  Game %d: " % g)
            if win2 < win1:
                print("%s win." % self.player1.name)
                win_record += "0"

            elif win1 < win2:
                print("%s win." % self.player2.name)
                win_record += "1"

            else:
                print("draw game.")
                win_record += "2"

            game_record.append(tuple(round_record))

        print("result: [%s] %d - %d [%s] (%d draw)" % (self.player1.name, win_record.count('0'),
                                                       win_record.count('1'), self.player2.name,
                                                       win_record.count('2')))

        if self.dumps:
            import uuid
            import gzip
            try:
                import cPickle as pickle
            except:
                import pickle

            filename = 'h2game_' + self.player1.name + '_vs_' + self.player2.name + str(uuid.uuid4())
            with gzip.open(filename + '.log.pkl.gz', 'wb') as pklfile:
                pickle.dump(self.player1.name, pklfile)
                pickle.dump(self.player2.name, pklfile)

                pickle.dump(win_record, pklfile)

                pickle.dump(game_record, pklfile)

            return filename, win_record.count('0'), win_record.count('1')

        return '', win_record.count('0'), win_record.count('1')
