import random

from Map.Agent import Agent
from Map.Item import Item


class Zombie(Agent):

    def __init__(self, description, dead_description, object_):
        super(Zombie, self).__init__(description, dead_description, object_)

    def hit(self, ctx, damage, msg):
        if self.health == 0:
            Item.hit(self, ctx, damage, msg)
        else:
            self.damage(ctx, damage)
            player_damage = 0
            if (self.health > 0):
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
