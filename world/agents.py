import random

from world.items import Item
from language.language_tools import list_of_words, add_indefinite_article


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


class Zombie(Agent):

    def __init__(self, description, dead_description, object_, weight):
        super(Zombie, self).__init__(description, dead_description, object_, weight)

    def hit(self, ctx, damage, msg):
        if self.health == 0:
            Item.hit(self, ctx, damage, msg)
        else:
            self.damage(ctx, damage)
            player_damage = 0
            if self.health > 0:
                msg = ' '.join([msg, 'The zombie snarls and takes a bite out of you.'])
                player_damage = random.randint(20, 30)
                ctx.hit(player_damage)
            else:
                msg = ' '.join([msg, 'The zombie keels over. Looks like it won\'t be getting up again.'])
            stats = [
                ctx.name,
                'damage: {}'.format(player_damage),
                'health: {}'.format(ctx.health),
                '', 'Zombie',
                'damage: {}'.format(damage),
                'health: {}'.format(self.health),
            ]
            ctx.console.print_block(msg, stats=stats)
