import random
import sys

from Map.Location import LOCATIONS


def unknown_object(ctx, verb, obj):
    ctx.console.print_block('I don\'t know how to {} "{}".'.format(verb, obj))


def exit_(cmd, ctx):
    if cmd.object:
        unknown_object(ctx, cmd.verb, cmd.object)
    else:
        ctx.console.print_block('Thanks for playing, {}.'.format(ctx.name))
        sys.exit(0)


def look(cmd, ctx):
    item = cmd.object
    if item in ctx.location.items:
        ctx.console.print_block(ctx.location.items[item].description)
    elif not item:
        ctx.console.print_block('Some longer description', title=ctx.location.description)
    else:
        unknown_object(ctx, 'look at', item)


def move(cmd, ctx):
    if not cmd.object:
        ctx.console.print_block('Where do you want to go?')
    elif cmd.object in ctx.location.directions:
        ctx.move(LOCATIONS, cmd.object)
        cmd.object = None
        look(cmd, ctx)
    else:
        unknown_object(ctx, 'go', cmd.object)


def hit(cmd, ctx):
    if not cmd.object:
        ctx.console.print_block('What do you want to hit?')
    elif cmd.object == 'zombie':
        damage = random.randint(20, 30)
        ctx.health -= damage
        stats = [
            'damage: {}'.format(damage),
            'health: {}'.format(ctx.health)
        ]
        ctx.console.print_block('You punch the zombie. The zombie snarls and takes a bite out of you.', stats=stats)
    else:
        unknown_object(ctx, cmd.verb, cmd.object)


def help_(cmd, ctx):
    if cmd.object and cmd.object != 'me':
        unknown_object(ctx, cmd.verb, cmd.object)
    else:
        ctx.console.print_block('Try entering a verb followed by an object.')


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
        ctx.console.print_block('I don\'t recognise the verb "' + cmd.verb + '".')
