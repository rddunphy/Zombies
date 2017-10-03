
class Location:
    def __init__(self, name, description, directions, items=None):
        self.name = name
        self.description = description
        self.directions = directions
        if items:
            self.items = items
        else:
            self.items = []
