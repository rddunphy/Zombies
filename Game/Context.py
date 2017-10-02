class Context:
    def __init__(self, name, location, console):
        self.name = name
        self.location = location
        self.console = console
        self.health = 100
        self.inventory = {}
        self.known_words = {'look', 'help', 'inventory', 'quit', 'go', 'north', 'south', 'east', 'west'}

    def move(self, locations, direction):
        loc = self.location.directions[direction]
        self.location = locations[loc]

    def available_items(self):
        return list(self.inventory.keys()) + list(self.location.items.keys())
