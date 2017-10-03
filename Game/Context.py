from Map.Map import Map


class Context:

    def __init__(self, name, console, dictionary):
        self.name = name
        self.map = Map(dictionary)
        self.location = self.map.locations[0]
        self.console = console
        self.health = 100
        self.inventory = []
        self.inventory_capacity = 60
        self.dictionary = dictionary
        self.known_words = {'look', 'help', 'inventory', 'quit', 'go', 'north', 'south', 'east', 'west'}

    def move(self, direction):
        loc = self.location.directions[direction]
        self.location = self.map.locations[loc]

    def available_items(self):
        return self.inventory + self.location.items

    def hit(self, damage):
        self.health -= damage

    def remaining_inventory_capacity(self):
        cap = self.inventory_capacity
        for item in self.inventory:
            cap -= item.weight
        return cap
