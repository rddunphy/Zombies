from Map.Map import Map


class Context:

    def __init__(self, name, console):
        self.name = name
        self.map = Map()
        self.location = self.map.locations[0]
        self.console = console
        self.health = 100
        self.inventory = []
        self.known_words = {'look', 'help', 'inventory', 'quit', 'go', 'north', 'south', 'east', 'west'}

    def move(self, direction):
        loc = self.location.directions[direction]
        self.location = self.map.locations[loc]

    def available_items(self):
        return self.inventory + self.location.items
