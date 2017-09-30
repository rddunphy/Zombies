import argparse
import random
import sys

from Map.Context import Context
from Map.Location import LOCATIONS
from Parser.Command import Command

VERBS = {
    'HELP': ['help'],
    'HIT': ['hit', 'punch'],
    'LOOK': ['look', 'examine', 'inspect', 'l'],
    'MOVE': ['go', 'walk', 'move'],
    'EXIT': ['exit', 'quit', 'q']
}

VERB_ALIASES = {}

for verb in VERBS:
    for alias in VERBS[verb]:
        VERB_ALIASES[alias] = verb


def parse(s):
    tokens = s.lower().split()
    verb = tokens[0]
    object_ = None
    if len(tokens) > 1:
        object_ = tokens[1]
    if verb in VERB_ALIASES:
        return Command(VERB_ALIASES[verb], object_)
    return Command(verb, object_)


def exit_(cmd, ctx):
    print('Thanks for playing, {}.'.format(ctx.name))
    sys.exit(0)


def look(cmd, ctx):
    print(ctx.location.description)
    print('You see a zombie. It looks hungry.')


def move(cmd, ctx):
    if not cmd.object:
        print('Where do you want to go?')
    elif cmd.object in ctx.location.directions:
        ctx.move(LOCATIONS, cmd.object)
        look(cmd, ctx)
    else:
        print('I don\'t know how to go "' + cmd.object + '"')


def hit(cmd, ctx):
    if cmd.object == None:
        print('What do you want to hit?')
    elif cmd.object == 'zombie':
        print('You punch the zombie. The zombie snarls and takes a bite out of you.')
        damage = random.randint(20, 30)
        ctx.health -= damage
        print('[damage: {}, health: {}]'.format(damage, ctx.health))
    else:
        print('I don\'t know how to hit "' + cmd.object + '".')


def help_(cmd, ctx):
    if cmd.object and cmd.object != 'me':
        print('I don\'t know how to help "' + cmd.object + '".')
    else:
        print('Try entering a verb followed by an object.')


def execute(cmd, ctx):
    if cmd.verb == 'EXIT':
        exit_(cmd, ctx)
    elif cmd.verb == 'LOOK':
        look(cmd, ctx)
    elif cmd.verb == 'MOVE':
        move(cmd, ctx)
    elif cmd.verb == 'HIT':
        hit(cmd, ctx)
    elif cmd.verb == 'HELP':
        help_(cmd, ctx)
    else:
        print('I don\'t recognise the verb "' + cmd.verb + '".')


def get_input():
    s = input('> ').strip()
    if len(s) > 0:
        return s
    return get_input()


def intro(ctx):
    print('You wake up with a headache. In front of you is a zombie.')


def game_over(ctx):
    print('{}, you are now a zombie.'.format(ctx.name))
    print('Enjoy your afterlife!')
    print('**** GAME OVER ****')
    sys.exit(0)


def repl(ctx):
    s = get_input()
    cmd = parse(s)
    execute(cmd, ctx)
    if ctx.health <= 0:
        game_over(ctx)
    else:
        repl(ctx)


def run():
    parser = argparse.ArgumentParser(description='A zombie game.')
    parser.add_argument('-n', '--name', type=str, nargs='+', help='your name')
    args = parser.parse_args()
    if args.name:
        name = ' '.join(args.name)
        print('Hello, {}!'.format(name))
    else:
        print('Hello, future zombie!')
        print('Please enter your name.')
        name = get_input()
        print('Hi, {}!'.format(name))
    ctx = Context(name, LOCATIONS[0])
    intro(ctx)
    repl(ctx)


if __name__ == '__main__':
    run()
