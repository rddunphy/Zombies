import random
import sys


def unknown_object(ctx, verb, obj):
    ctx.console.print_block('There is no {} to {}.'.format(str(obj), str(verb)))


def ambiguous_object(ctx, verb, obj):
    ctx.console.print_block('There\'s more than one {} to {}.'.format(str(obj), str(verb)))


def locate_object(ctx, obj):
    candidates = []
    for item in ctx.location.items:
        if item == obj:
            candidates.append(item)
    for item in ctx.inventory:
        if item == obj:
            candidates.append(item)
    return candidates


def exit_(cmd, ctx):
    if cmd.direct:
        unknown_object(ctx, cmd.verb, cmd.direct)
    else:
        ctx.console.print_block('Thanks for playing, {}.'.format(ctx.name))
        sys.exit(0)


def view_surroundings(ctx):
    ctx.console.print_block(ctx.location.description, title=ctx.location.name)


def look(cmd, ctx):
    obj = cmd.direct
    if not obj:
        view_surroundings(ctx)
    else:
        items = locate_object(ctx, obj)
        if not items:
            unknown_object(ctx, cmd.verb, obj)
        elif len(items) == 1:
            ctx.console.print_block(items[0].description)
        elif obj.plural:
            for item in items:
                ctx.console.print_block(item.description)
        else:
            ambiguous_object(ctx, cmd.verb, obj)


def take(cmd, ctx):
    obj = cmd.direct
    if not obj:
        ctx.console.print_block('What do you want to pick up?')
    else:
        items = locate_object(ctx, obj)
        if not items:
            unknown_object(ctx, cmd.verb, obj)
        elif len(items) == 1:
            item = items[0]
            ctx.inventory.append(item)
            ctx.location.items.remove(item)
            ctx.console.print_block('You pick up the {}.'.format(item))
        elif obj.plural:
            for item in items:
                ctx.inventory.append(item)
                ctx.location.items.remove(item)
                ctx.console.print_block('You pick up the {}.'.format(item))
        else:
            ambiguous_object(ctx, cmd.verb, obj)


def inventory(cmd, ctx):
    if not ctx.inventory:
        ctx.console.print_block('You have nothing in your inventory.')
    else:
        items = [str(item) for item in ctx.inventory]
        ctx.console.print_block('Your inventory contains:', stats=items)


def move(cmd, ctx):
    if not cmd.direction:
        ctx.console.print_block('Where do you want to go?')
    else:
        if cmd.direction in ctx.location.directions.keys():
            ctx.move(cmd.direction)
            view_surroundings(ctx)
        else:
            ctx.console.print_block('There\'s no way to go {} from here.'.format(cmd.direction.value))


def hit(cmd, ctx):
    obj = cmd.direct
    if not obj:
        ctx.console.print_block('What do you want to hit?')
    else:
        items = locate_object(ctx, obj)
        if not items:
            unknown_object(ctx, cmd.verb, obj)
        elif len(items) == 1:
            target = items[0]
            obj2 = cmd.using
            if not obj2:
                damage = random.randint(10, 20)
                target.hit(ctx, damage, 'You punch the {}.'.format(str(target)))
            else:
                weapons = locate_object(ctx, obj2)
                if not weapons:
                    ctx.console.print_block('You don\'t have a {}.'.format(str(obj2)))
                elif len(weapons) == 1:
                    weapon = weapons[0]
                    damage = random.randint(40, 50)
                    target.hit(ctx, damage, 'You hit the {} with the {}.'.format(str(target), str(weapon)))
                elif obj2.plural:
                    ctx.console.print_block('You can only use one weapon at a time.')
                else:
                    ambiguous_object(ctx, 'use', obj2)
        elif obj.plural:
            ctx.console.print_block('You can only hit one thing at a time.')
        else:
            ambiguous_object(ctx, cmd.verb, obj)


def help_(cmd, ctx):
    ctx.console.print_block('Try entering a verb followed by an object.')


def give(cmd, ctx):
    print('giving not yet implemented')
