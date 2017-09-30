import random
import sys

from Map.Location import LOCATIONS


def unknown_object(verb, obj):
    print('I don\'t know how to ' + verb + ' "' + obj + '".')


def exit_(cmd, ctx):
    if cmd.object:
        unknown_object(cmd.verb, cmd.object)
    else:
        print('Thanks for playing, {}.'.format(ctx.name))
        sys.exit(0)


def look(cmd, ctx):
    item = cmd.object
    if item in ctx.location.items:
        print(ctx.location.items[item].description)
    elif not item:
        print(ctx.location.description)
        print('You see a zombie. It looks hungry.')
    else:
        unknown_object('look at', item)


def move(cmd, ctx):
    if not cmd.object:
        print('Where do you want to go?')
    elif cmd.object in ctx.location.directions:
        ctx.move(LOCATIONS, cmd.object)
        look(cmd, ctx)
    else:
        unknown_object('go', cmd.object)


def hit(cmd, ctx):
    if not cmd.object:
        print('What do you want to hit?')
    elif cmd.object == 'zombie':
        print('You punch the zombie. The zombie snarls and takes a bite out of you.')
        damage = random.randint(20, 30)
        ctx.health -= damage
        print('[damage: {}, health: {}]'.format(damage, ctx.health))
    else:
        unknown_object(cmd.verb, cmd.object)


def help_(cmd):
    if cmd.object and cmd.object != 'me':
        unknown_object(cmd.verb, cmd.object)
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
        help_(cmd)
    else:
        print('I don\'t recognise the verb "' + cmd.verb + '".')
