import random

from world.items import Item
from language.language_tools import list_of_words, add_indefinite_article, capitalise_first_letter


class Agent(Item):
    def __init__(self, name, description, dead_description, weight, nouns, short_name=None, adjectives=None,
                 items=None):
        super(Agent, self).__init__(name, description, weight, nouns, short_name=short_name, adjectives=adjectives)
        self.dead_description = dead_description
        self.health = 100
        if items:
            self.items = items
        else:
            self.items = []

    def is_dead(self):
        return self.health == 0

    def damage(self, ctx, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.adjectives.add(ctx.dictionary.get('dead'))
            self.name = ' '.join(['dead', self.name])

    def take_from(self, ctx, item):
        if self.is_dead():
            return Item.take_from(self, ctx, item)
        ctx.console.print_block(
            'You try and take the {} from the {}. It doesn\'t seem to want to give it up without a fight.'.format(
                item.short_name, self.short_name))
        return False

    def receive(self, ctx, item, msg):
        if not self.is_dead():
            ctx.console.print_block(' '.join([msg, 'It takes the {} without thanking you.'.format(item.short_name)]))
            self.items.append(item)
        else:
            ctx.console.print_block(
                ' '.join([msg,
                          'It is not in a fit state to receive gifts at the moment, and drops the {} on the ground.'.format(
                              item.short_name)]))
            ctx.location.items.append(item)

    def get_description(self, ctx):
        description = self.description
        if self.is_dead():
            description = self.dead_description
        if self.items:
            s = list_of_words([add_indefinite_article(ctx.dictionary, str(item)) for item in self.items])
            return ' '.join([description, 'It has {}.'.format(s)])
        else:
            return description


class Zombie(Agent):
    def __init__(self, dictionary, name, description, dead_description, weight, nouns=None, short_name='zombie',
                 adjectives=None):
        if not nouns:
            nouns = set()
        nouns.add(dictionary.get('zombie'))
        super(Zombie, self).__init__(name, description, dead_description, weight, nouns, short_name=short_name,
                                     adjectives=adjectives)

    def hit(self, ctx, damage, msg):
        if self.health == 0:
            Item.hit(self, ctx, damage, msg)
        else:
            self.damage(ctx, damage)
            player_damage = 0
            if self.health > 0:
                msg = ' '.join([msg, 'The {} snarls and takes a bite out of you.'.format(self.short_name)])
                player_damage = random.randint(20, 30)
                ctx.hit(player_damage)
            else:
                msg = ' '.join(
                    [msg, 'The {} keels over. Looks like it won\'t be getting up again.'.format(self.short_name)])
            stats = [
                ctx.name,
                'damage: {}'.format(player_damage),
                'health: {}'.format(ctx.health),
                '', capitalise_first_letter(self.name),
                'damage: {}'.format(damage),
                'health: {}'.format(self.health),
            ]
            ctx.console.print_block(msg, stats=stats)


class BankerZombie(Zombie):
    def __init__(self, dictionary):
        name = 'banker zombie'
        description = ('The cross-eyed zombie is ignoring you. He appears to have been a fat banker at one '
                       'point, but is now only interested in the handful of brains he is currently nibbling on.')
        dead_description = 'The zombie is lying on the ground in pieces. A maggot is crawling out of its left ear.'
        weight = 95
        nouns = {dictionary.get('banker zombie'), dictionary.get('banker')}
        adjectives = {dictionary.get('fat'), dictionary.get('cross-eyed')}
        super(BankerZombie, self).__init__(dictionary, name, description, dead_description, weight, nouns=nouns,
                                           adjectives=adjectives)
