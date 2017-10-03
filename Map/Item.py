from Parser.Object import Object


class Item:

    def __init__(self, description, object_):
        self.description = description
        self.object = object_

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.description == other.description
        elif isinstance(other, Object):
            return other.noun == self.object.noun and other.plural == self.object.plural and other.adjectives <= self.object.adjectives
        else:
            return False

    def __str__(self):
        return str(self.object)

    def hit(self, ctx):
        ctx.console.print_block('Nothing interesting happens.')
