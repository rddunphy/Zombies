import sys

from game.actions import Position
from game.console import Console
from language.dictionary import Dictionary
from language.parser import Parser, ParseError
from world.locations import build_map


def _intro(ctx):
    ctx.console.print_block([
        'Hello, {}!'.format(ctx.name),
        ('You wake up with a headache. You appear to be lying on cobbled ground. It\'s raining. You think you may '
         'have been hit over the head, but you can\'t remember how you got here.')
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
        self.location = build_map(dictionary)
        self.console = console
        self.health = 100
        self.inventory = []
        self.inventory_capacity = 60
        self.position = Position.LYING
        self.dictionary = dictionary
        self.known_words = {'look', 'help', 'inventory', 'quit', 'go', 'north', 'south', 'east', 'west'}

    def move(self, direction):
        self.location = self.location.directions[direction]

    def available_items(self):
        return self.inventory + self.location.items

    def hit(self, damage):
        self.health -= damage

    def remaining_inventory_capacity(self):
        cap = self.inventory_capacity
        for item in self.inventory:
            cap -= item.weight
        return cap
