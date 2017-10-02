from Map.Item import Item


class Agent(Item):

    def __init__(self, description):
        super(Agent, self).__init__(description)
        self.health = 100
