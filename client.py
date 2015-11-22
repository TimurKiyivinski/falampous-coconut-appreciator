#!/bin/env python3
import game
import argparse, time, string, random
from multiprocessing import Process

class Input():
    def __init__(self):
        pass
    def get(self):
        return input()

class View():
    def __init__(self):
        pass
    def message(self, text):
        try:
            print(text)
        except Exception as e:
            print(e)
    def board(self, board, player):
        for i in range(0, board.height):
            print("X %i\t:" % i, end='')
            for ii in range(0, board.width):
                if (board.tokens[i][ii] == 0):
                    print(" %i .," % ii, end='')
                else:
                    if board.tokens[i][ii].player.id == player.id:
                        print(" %i %s%s" % (ii, board.tokens[i][ii].token, "+"), end='')
                    else:
                        print(" %i %s%s" % (ii, board.tokens[i][ii].token, "-"), end='')
            print('\n', end='')

def main(args):
    # Create View and Input classes
    user_view = View()
    user_input = Input()
    # ClientState
    client = game.ClientState()
    client.setIO(user_view, user_input)
    # Server connection and listener
    if not args.debug:
        client.connect(args.server, args.port)
        #listener = Process(target=client.listen)
        #listener.start()
        connection = Process(target=client.start)
        connection.start()
        client.listen()
    else:
        user_view.message('User input:')
        text = user_input.get()
        user_view.message("> %s" % text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Medieval Battle Chess client application.')
    parser.add_argument('-s', '--server', help='Server IP', default='127.0.0.1', required=False)
    parser.add_argument('-p', '--port', help='Server Port', default='4096', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose logging', action='store_true')
    parser.add_argument('-d', '--debug', help='Enable debugging', action='store_true')
    args = parser.parse_args()
    main(args)
