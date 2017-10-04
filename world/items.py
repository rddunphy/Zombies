from language.language_tools import build_object
from language.words import Object


class Item:
    def __init__(self, description, object_, weight):
        self.description = description
        self.object = object_
        self.weight = weight

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.description == other.description
        elif isinstance(other, Object):
            return other.noun == self.object.noun and other.plural == self.object.plural and other.adjectives <= self.object.adjectives
        else:
            return False

    def __str__(self):
        return str(self.object)

    def hit(self, ctx, damage, msg):
        ctx.console.print_block(' '.join([msg, 'Nothing interesting happens.']))

    def receive(self, ctx, item, msg):
        ctx.console.print_block(' '.join([msg, 'It\'s and inanimate object, so it doesn\'t seem interested.']))
        ctx.location.items.append(item)

    def get_description(self, ctx):
        return self.description


class WoodenBoard(Item):
    def __init__(self, dictionary):
        object_ = build_object(dictionary, 'wooden board')
        super(WoodenBoard, self).__init__('It\'s a fairly plain but sturdy plank of wood.', object_, 2)
