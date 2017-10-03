import sys

from Game.Console import Console
from Game.Context import Context
from Parser.Dictionary import Dictionary
from Parser.Parser import Parser, ParseError


def intro(ctx):
    ctx.console.print_block([
        'Hello, {}!'.format(ctx.name),
        'You wake up with a headache.'
    ])


def game_over(ctx):
    ctx.console.print_block([
        '{}, you are now a zombie.'.format(ctx.name),
        'Enjoy your afterlife!'
    ])
    ctx.console.print_info('**** GAME OVER ****')
    ctx.console.empty_line()
    sys.exit(0)


def repl(parser, ctx):
    s = ctx.console.get_input(ctx)
    try:
        cmds = parser.parse(s, ctx)
        for cmd in cmds:
            cmd.verb.fn(cmd, ctx)
    except ParseError as err:
        ctx.console.print_block(str(err))
    if ctx.health <= 0:
        game_over(ctx)
    else:
        repl(parser, ctx)


def start_game(name, plaintext):
    console = Console(plaintext)
    if not name:
        console.print_block([
            'Hello, future zombie!',
            'Please enter your name.'
        ])
        name = console.get_input(None)
    dictionary = Dictionary()
    ctx = Context(name, console, dictionary)
    intro(ctx)
    repl(Parser(dictionary), ctx)
