from Map.Agent import Agent
from Map.Item import Item


class Location:
    def __init__(self, name, description, directions, items):
        self.name = name
        self.description = description
        self.directions = directions
        self.items = items


LOCATIONS = {
    0: Location("Centre of square",
                'You are in the centre of a large square. There is a wooden board on the ground next to you.',
                {'north': 1, 'south': 2, 'east': 3, 'west': 4},
                {'board': Item('It\'s a fairly plain but sturdy plank of wood.')}),
    1: Location("North side of square", 'You are on the north side of the square. You see a zombie.',
                {'south': 0, 'east': 3, 'west': 4},
                {'zombie': Agent('The cross-eyed zombie seems to be ignoring you. He appears to have been a banker.')}),
    2: Location("South side of square", 'You are on the south side of the square. There are buildings.',
                {'north': 0, 'east': 3, 'west': 4}, {}),
    3: Location("East side of square", 'You are on the east side of the square. There are buildings.',
                {'west': 0, 'north': 1, 'south': 2}, {}),
    4: Location("West side of square", 'You are on the west side of the square. There are buildings.',
                {'east': 0, 'north': 1, 'south': 2}, {})
}
