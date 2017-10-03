from Map.Item import Item


class Agent(Item):

    def __init__(self, description, object_):
        super(Agent, self).__init__(description, object_)
        self.health = 100
