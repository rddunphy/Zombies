from Map.Item import Item


class Location:
    def __init__(self, description, directions, items):
        self.description = description
        self.directions = directions
        self.items = items


LOCATIONS = {
    0: Location("Centre of square", {'north': 1, 'south': 2, 'east': 3, 'west': 4}, {'board': Item('Wooden board')}),
    1: Location("North side of square", {'south': 0, 'east': 3, 'west': 4}, {}),
    2: Location("South side of square", {'north': 0, 'east': 3, 'west': 4}, {}),
    3: Location("East side of square", {'west': 0, 'north': 1, 'south': 2}, {}),
    4: Location("West side of square", {'east': 0, 'north': 1, 'south': 2}, {})
}
