#!/bin/env python3
import game
import json

def config(config_file = 'config.json'):
    """
    Read configuration file.
    """
    data = json.load(open(config_file))
    return data['board'], data['tokens'], data['port']
    pass

def main():
    """
    Start game.
    """
    board, tokens, port = config()
    GameState = game.GameState(board, tokens, port)
    try:
        GameState.start()
    except KeyboardInterrupt:
        return False

if __name__ == '__main__':
    main()
