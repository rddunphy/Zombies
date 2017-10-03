import random

from Map.Agent import Agent


class Zombie(Agent):

    def __init__(self, description, object_):
        super(Zombie, self).__init__(description, object_)
        self.health = 100

    def hit(self, ctx):
        damage = random.randint(20, 30)
        ctx.health -= damage
        stats = [
            'damage: {}'.format(damage),
            'health: {}'.format(ctx.health)
        ]
        ctx.console.print_block('You punch the zombie. The zombie snarls and takes a bite out of you.', stats=stats)
