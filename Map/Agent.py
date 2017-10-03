from Map.Item import Item
from Parser.language_tools import list_of_words, add_indefinite_article


class Agent(Item):

    def __init__(self, description, dead_description, object_, weight):
        super(Agent, self).__init__(description, object_, weight)
        self.dead_description = dead_description
        self.health = 100
        self.items = []

    def damage(self, ctx, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.object.adjectives.add(ctx.dictionary.get('dead'))
            self.description = self.dead_description

    def receive(self, ctx, item, msg):
        ctx.console.print_block(' '.join([msg, 'It takes the {} without thanking you.'.format(item)]))
        self.items.append(item)

    def get_description(self, ctx):
        if self.items:
            s = list_of_words([add_indefinite_article(ctx.dictionary, str(item)) for item in self.items])
            return ' '.join([self.description, 'It has {}.'.format(s)])
        else:
            return Item.get_description(self, ctx)
