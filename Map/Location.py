class Location:
    def __init__(self, description, directions):
        self.description = description
        self.directions = directions


LOCATIONS = {
    0: Location("Centre of square", {'north': 1, 'south': 2, 'east': 3, 'west': 4}),
    1: Location("North side of square", {'south': 0, 'east': 3, 'west': 4}),
    2: Location("South side of square", {'north': 0, 'east': 3, 'west': 4}),
    3: Location("East side of square", {'west': 0, 'north': 1, 'south': 2}),
    4: Location("West side of square", {'east': 0, 'north': 1, 'south': 2})
}
