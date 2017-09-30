import sys

from Game.Context import Context
from Game.Executor import print_block, execute
from Map.Location import LOCATIONS
from Parser.Parser import Parser


def intro(ctx):
    print_block([
        'Hello, {}!'.format(ctx.name),
        'You wake up with a headache. In front of you is a zombie.'
    ])


def game_over(ctx):
    print_block([
        '{}, you are now a zombie.'.format(ctx.name),
        'Enjoy your afterlife!',
        '**** GAME OVER ****'
    ])
    sys.exit(0)


def get_input():
    s = input('> ').strip()
    if len(s) > 0:
        return s
    return get_input()


def repl(parser, ctx):
    s = get_input()
    cmd = parser.parse(s)
    execute(cmd, ctx)
    if ctx.health <= 0:
        game_over(ctx)
    else:
        repl(parser, ctx)


def start_game(name):
    if not name:
        print_block([
            'Hello, future zombie!',
            'Please enter your name.'
        ])
        name = get_input()
    ctx = Context(name, LOCATIONS[0])
    intro(ctx)
    repl(Parser(), ctx)
