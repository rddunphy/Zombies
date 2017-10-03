from Map.Item import Item


class Agent(Item):

    def __init__(self, description, dead_description, object_):
        super(Agent, self).__init__(description, object_)
        self.dead_description = dead_description
        self.health = 100

    def damage(self, ctx, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.object.adjectives.add(ctx.dictionary.adjectives['dead'])
            self.description = self.dead_description