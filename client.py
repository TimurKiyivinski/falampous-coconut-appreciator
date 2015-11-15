#!/bin/env python3
import game
import argparse

def main(args):
    while True:
        try:
            client = game.ClientState()
            client.start(args.server, args.port)
        except KeyboardInterrupt:
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Medieval Battle Chess client application.')
    parser.add_argument('-s', '--server', help='Server IP', default='127.0.0.1', required=False)
    parser.add_argument('-p', '--port', help='Server Port', default='4096', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose logging', action='store_true')
    args = parser.parse_args()
    main(args)
