if __name__ == "__main__":
    import h2game

    params = h2game.setup()

    try:
        game = h2game.H2Game(**params)
        filename, win1, win2 = game.play_the_game()

        if params['dumps']:
            import viz
            viz.dump2img(filename)

    except:
        import sys
        import traceback

        info = sys.exc_info()
        if info[1] != sys.exit(0):
            print(info[1])
            print("".join(traceback.format_tb(info[2])).rstrip())
