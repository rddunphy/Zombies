import random
import sys


def unknown_object(ctx, verb, obj):
    ctx.console.print_block('There is no {} to {}.'.format(str(obj), str(verb)))


def ambiguous_object(ctx, verb, obj):
    ctx.console.print_block('There\'s more than one {} to {}.'.format(str(obj), str(verb)))


def locate_object_in_inventory(ctx, obj):
    candidates = []
    for item in ctx.inventory:
        if item == obj:
            candidates.append(item)
    return candidates


def locate_object_in_location(ctx, obj):
    candidates = []
    for item in ctx.location.items:
        if item == obj:
            candidates.append(item)
    return candidates


def locate_object_anywhere(ctx, obj):
    return locate_object_in_inventory(ctx, obj) + locate_object_in_location(ctx, obj)


def exit_(cmd, ctx):
    if cmd.direct:
        unknown_object(ctx, cmd.verb, cmd.direct)
    else:
        ctx.console.print_block('Thanks for playing, {}.'.format(ctx.name))
        sys.exit(0)


def view_surroundings(ctx):
    ctx.console.print_block(ctx.location.get_description(ctx), title=ctx.location.name)


def look(cmd, ctx):
    obj = cmd.direct
    if not obj:
        view_surroundings(ctx)
    else:
        items = locate_object_anywhere(ctx, obj)
        if not items:
            unknown_object(ctx, cmd.verb, obj)
        elif len(items) == 1:
            ctx.console.print_block(items[0].description)
        elif obj.plural:
            for item in items:
                ctx.console.print_block(item.description)
        else:
            ambiguous_object(ctx, cmd.verb, obj)


def take_item(ctx, item):
    if (item.weight > ctx.inventory_capacity):
        ctx.console.print_block('The {} is to heavy to lift.'.format(str(item)))
    elif (item.weight > ctx.remaining_inventory_capacity()):
        ctx.console.print_block('There is not enough space in your inventory for the {}.'.format(str(item)))
    else:
        ctx.inventory.append(item)
        ctx.location.items.remove(item)
        ctx.console.print_block('You pick up the {}.'.format(item))


def take(cmd, ctx):
    obj = cmd.direct
    items = locate_object_in_location(ctx, obj)
    if not items:
        unknown_object(ctx, cmd.verb, obj)
    elif len(items) == 1:
        take_item(ctx, items[0])
    elif obj.plural:
        for item in items:
            take_item(ctx, item)
    else:
        ambiguous_object(ctx, cmd.verb, obj)


def drop_item(ctx, item):
    ctx.inventory.remove(item)
    ctx.location.items.append(item)
    ctx.console.print_block('You drop the {}.'.format(item))


def drop(cmd, ctx):
    obj = cmd.direct
    items = locate_object_in_inventory(ctx, obj)
    if not items:
        unknown_object(ctx, cmd.verb, obj)
    elif len(items) == 1:
        drop_item(ctx, items[0])
    elif obj.plural:
        for item in items:
            drop_item(ctx, item)
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


def run(cmd, ctx):
    if not cmd.direction:
        ctx.console.print_block('Where do you want to run to?')
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
        items = locate_object_anywhere(ctx, obj)
        if not items:
            unknown_object(ctx, cmd.verb, obj)
        elif len(items) == 1:
            target = items[0]
            obj2 = cmd.using
            if not obj2:
                damage = random.randint(10, 20)
                target.hit(ctx, damage, 'You punch the {}.'.format(str(target)))
            else:
                weapons = locate_object_in_inventory(ctx, obj2)
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
