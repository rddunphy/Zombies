#!/usr/bin/env python3

"""Zombies is a Zork-style console game set in the bonnie town of Glasgow."""

import argparse

from game.game import start_game


__author__ = "R. David Dunphy"
__license__ = "MIT"
__version__ = "Zombies v0.01"
__email__ = "rdd.dunphy@gmail.com"


def run():
    parser = argparse.ArgumentParser(description='A zombie game.')
    parser.add_argument('-n', '--name', type=str, nargs='+', help='supply your name')
    parser.add_argument('--version', action='store_true', help='show version information')
    parser.add_argument('--plaintext', action='store_true', help='display output without ANSI formatting')
    args = parser.parse_args()
    if args.version:
        print(__doc__)
        print(__version__ + " created by " + __author__)
    else:
        name = None
        if args.name:
            name = ' '.join(args.name)
        start_game(name, args.plaintext)


if __name__ == '__main__':
    run()
