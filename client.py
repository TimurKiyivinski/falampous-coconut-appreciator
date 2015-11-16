#!/bin/env python3
import game
import argparse, time
from multiprocessing import Process

def main(args):
    try:
        client = game.ClientState()
        client.connect(args.server, args.port)
        listener = Process(target=client.listen)
        listener.start()
        print('Waiting 10 seconds to connect.')
        time.sleep(10)
        print('Connect.')
        client.start()
        listener.join()
    except KeyboardInterrupt:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Medieval Battle Chess client application.')
    parser.add_argument('-s', '--server', help='Server IP', default='127.0.0.1', required=False)
    parser.add_argument('-p', '--port', help='Server Port', default='4096', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose logging', action='store_true')
    args = parser.parse_args()
    main(args)
