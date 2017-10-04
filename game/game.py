import sys

from game.console import Console
from world.map import Map
from language.dictionary import Dictionary
from language.parser import Parser, ParseError


def _intro(ctx):
    ctx.console.print_block([
        'Hello, {}!'.format(ctx.name),
        'You wake up with a headache.'
    ])


def _game_over(ctx):
    ctx.console.print_block([
        '{}, you are now a zombie.'.format(ctx.name),
        'Enjoy your afterlife!'
    ])
    ctx.console.print_info('**** GAME OVER ****')
    ctx.console.empty_line()
    sys.exit(0)


def _repl(parser, ctx):
    s = ctx.console.get_input(ctx)
    try:
        cmds = parser.parse(s, ctx)
        for cmd in cmds:
            cmd.verb.fn(cmd, ctx)
    except ParseError as err:
        ctx.console.print_block(str(err))
    if ctx.health <= 0:
        _game_over(ctx)
    else:
        _repl(parser, ctx)


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
    _intro(ctx)
    _repl(Parser(dictionary), ctx)


class Context:

    def __init__(self, name, console, dictionary):
        self.name = name
        self.map = Map(dictionary)
        self.location = self.map.locations[0]
        self.console = console
        self.health = 100
        self.inventory = []
        self.inventory_capacity = 60
        self.dictionary = dictionary
        self.known_words = {'look', 'help', 'inventory', 'quit', 'go', 'north', 'south', 'east', 'west'}

    def move(self, direction):
        loc = self.location.directions[direction]
        self.location = self.map.locations[loc]

    def available_items(self):
        return self.inventory + self.location.items

    def hit(self, damage):
        self.health -= damage

    def remaining_inventory_capacity(self):
        cap = self.inventory_capacity
        for item in self.inventory:
            cap -= item.weight
        return cap
