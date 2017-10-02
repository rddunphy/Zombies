import random
import sys

from Map.Location import LOCATIONS


def unknown_object(ctx, verb, obj):
    ctx.console.print_block('I don\'t know how to {} "{}".'.format(verb, obj))


def exit_(cmd, ctx):
    if cmd.direct:
        unknown_object(ctx, cmd.verb, cmd.direct)
    else:
        ctx.console.print_block('Thanks for playing, {}.'.format(ctx.name))
        sys.exit(0)


def look(cmd, ctx):
    item = cmd.direct
    if not item:
        ctx.console.print_block(ctx.location.description, title=ctx.location.name)
    elif item.token in ctx.location.items:
        ctx.console.print_block(ctx.location.items[item.token].description)
    else:
        unknown_object(ctx, 'look at', item)


def take(cmd, ctx):
    item = cmd.direct
    if not item:
        ctx.console.print_block('What do you want to pick up?')
    elif item.token in ctx.location.items:
        ctx.inventory[item.token] = ctx.location.items[item.token]
        del ctx.location.items[item.token]
        ctx.console.print_block('You pick up the {}'.format(item))
    else:
        unknown_object(ctx, 'pick up', item)


def inventory(cmd, ctx):
    if cmd.direct:
        unknown_object(cmd, cmd.verb, cmd.direct)
    else:
        ctx.console.print_block('Your inventory contains:', stats=ctx.inventory.keys())


def move(cmd, ctx):
    if not cmd.direct:
        ctx.console.print_block('Where do you want to go?')
    elif cmd.direct.token in ctx.location.directions:
        ctx.move(LOCATIONS, cmd.direct.token)
        cmd.direct = None
        look(cmd, ctx)
    else:
        unknown_object(ctx, 'go', cmd.direct)


def hit(cmd, ctx):
    if not cmd.direct:
        ctx.console.print_block('What do you want to hit?')
    elif cmd.direct.token == 'zombie':
        damage = random.randint(20, 30)
        ctx.health -= damage
        stats = [
            'damage: {}'.format(damage),
            'health: {}'.format(ctx.health)
        ]
        ctx.console.print_block('You punch the zombie. The zombie snarls and takes a bite out of you.', stats=stats)
    else:
        unknown_object(ctx, cmd.verb, cmd.direct)


def help_(cmd, ctx):
    if cmd.direct and cmd.direct.token != 'me':
        unknown_object(ctx, cmd.verb, cmd.direct)
    else:
        ctx.console.print_block('Try entering a verb followed by an object.')


def give(cmd, ctx):
    print('giving not yet implemented')


def execute(cmd, ctx):
    cmd.verb.fn(cmd, ctx)
