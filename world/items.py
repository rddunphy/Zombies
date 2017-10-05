from language.words import Object


class Item:
    def __init__(self, name, description, weight, nouns, short_name=None, adjectives=None, plural=False, items=None):
        self.name = name
        self.description = description
        self.nouns = nouns
        if adjectives:
            self.adjectives = adjectives
        else:
            self.adjectives = set()
        self.weight = weight
        if not short_name:
            self.short_name = name
        else:
            self.short_name = short_name
        if not items:
            self.items = []
        else:
            self.items = items
        self.plural = plural

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.description == other.description
        elif isinstance(other, Object):
            return other.noun in self.nouns and other.plural == self.plural and other.adjectives <= self.adjectives
        else:
            return False

    def __str__(self):
        return str(self.name)

    def hit(self, ctx, damage, msg):
        ctx.console.print_block(' '.join([msg, 'Nothing interesting happens.']))

    def locate_in_items(self, obj):
        candidates = []
        for item in self.items:
            if item == obj:
                candidates.append(item)
        return candidates

    def take_from(self, ctx, item):
        ctx.console.print_block('You take the {} from the {}.'.format(item.short_name, self.short_name))
        self.items.remove(item)
        return True

    def receive(self, ctx, item, msg):
        ctx.console.print_block(' '.join([msg, 'It\'s and inanimate object, so it doesn\'t seem interested.']))
        ctx.location.items.append(item)

    def get_description(self, ctx):
        return self.description


class WoodenBoard(Item):
    def __init__(self, dictionary):
        name = 'wooden board'
        short_name = 'board'
        description = ('It\'s a fairly plain but sturdy plank of wood. There is some dried blood at one end of it. '
                       'Perhaps it was used to hit someone over the head.')
        nouns = {dictionary.get('board')}
        adjectives = {dictionary.get('wooden'), dictionary.get('blood-stained')}
        weight = 2
        super(WoodenBoard, self).__init__(name, description, weight, nouns, short_name=short_name,
                                          adjectives=adjectives)
