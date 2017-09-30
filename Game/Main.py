from Game.Context import Context
from Game.REPL import intro, repl, get_input
from Map.Location import LOCATIONS
from Parser.Parser import Parser


def start_game(name):
    if not name:
        print('Hello, future zombie!')
        print('Please enter your name.')
        name = get_input()
    print('Hello, {}!'.format(name))
    ctx = Context(name, LOCATIONS[0])
    intro()
    repl(Parser(), ctx)
