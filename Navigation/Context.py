class Context:
    def __init__(self, name, location):
        self.name = name
        self.health = 100
        self.location = location

    def move(self, locations, direction):
        loc = self.location.directions[direction]
        self.location = locations[loc]
