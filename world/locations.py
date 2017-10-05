from enum import Enum

from language.language_tools import list_of_words, add_indefinite_article, capitalise_first_letter
from world.furnishings import Furnishing, CobbledGround, TarmacGround, LionStatue
from world.items import WoodenBoard
from world.agents import Agent, BankerZombie


class Direction(Enum):
    N = 'north'
    NE = 'north-east'
    E = 'east'
    SE = 'south-east'
    S = 'south'
    SW = 'south-west'
    W = 'west'
    NW = 'north-west'
    UP = 'up'
    DN = 'down'


class Location:
    def __init__(self, name, description, directions, items):
        self.name = name
        self.description = description
        self.directions_classes = {}
        self.directions = {}
        self.items = items
        self._assign_directions_classes(directions)

    def _assign_directions_classes(self, location_classes):
        if len(location_classes) != 8 and len(location_classes) != 10:
            raise Exception('This method requires a list of either 8 or 10 locations.')
        self.directions_classes[Direction.N] = location_classes[0]
        self.directions_classes[Direction.NE] = location_classes[1]
        self.directions_classes[Direction.E] = location_classes[2]
        self.directions_classes[Direction.SE] = location_classes[3]
        self.directions_classes[Direction.S] = location_classes[4]
        self.directions_classes[Direction.SW] = location_classes[5]
        self.directions_classes[Direction.W] = location_classes[6]
        self.directions_classes[Direction.NW] = location_classes[7]
        if len(location_classes) == 10:
            self.directions_classes[Direction.UP] = location_classes[8]
            self.directions_classes[Direction.DN] = location_classes[9]

    def get_description(self, ctx):
        sentences = [self.description]
        things = [item for item in self.items if not isinstance(item, Agent) and not isinstance(item, Furnishing)]
        agents = [item for item in self.items if isinstance(item, Agent)]
        if things:
            s = list_of_words([add_indefinite_article(ctx.dictionary, str(item)) for item in things])
            verb = 'is'
            if len(things) > 1:
                verb = 'are'
            sentences.append('{} {} lying on the ground.'.format(capitalise_first_letter(s), verb))
        if agents:
            s = list_of_words([add_indefinite_article(ctx.dictionary, str(agent)) for agent in agents])
            sentences.append('You see {}.'.format(s))
        return ' '.join(sentences)


class TownSquareCentre(Location):
    def __init__(self, dictionary):
        name = 'Town square'
        description = ('You are in the centre of a large square surrounded by buildings. To the east is a large statue '
                       'of a lion. To the north you see someone who appears to be eating something. He doesn\'t look '
                       'very well.')
        directions = [
            TownSquareNorth, TownSquareNorthEast, TownSquareEast, TownSquareSouthEast, TownSquareSouth,
            TownSquareSouthWest, TownSquareWest, TownSquareNorthWest
        ]
        items = [WoodenBoard(dictionary), CobbledGround(dictionary)]
        super(TownSquareCentre, self).__init__(name, description, directions, items)


class TownSquareNorth(Location):
    def __init__(self, dictionary):
        name = 'North side of town square'
        description = ('You are on the north side of a square. To the north is a boarded up building. A street runs '
                       'east to west.')
        directions = [
            'There\'s no way into that building.', None, TownSquareNorthEast, TownSquareEast, TownSquareCentre,
            TownSquareWest, TownSquareNorthWest, None
        ]
        items = [BankerZombie(dictionary)]
        super(TownSquareNorth, self).__init__(name, description, directions, items)


class TownSquareNorthEast(Location):
    def __init__(self, dictionary):
        name = 'North-east corner of town square'
        description = 'You are in the north-east corner of a square. Streets leave the square to the north and east.'
        directions = [None, None, None, None, TownSquareEast, TownSquareCentre, TownSquareNorth, None]
        items = [CobbledGround(dictionary)]
        super(TownSquareNorthEast, self).__init__(name, description, directions, items)


class TownSquareEast(Location):
    def __init__(self, dictionary):
        name = 'East side of town square'
        description = ('You are at the eastern end of a square. A large statue of a lion dominates this area. Behind '
                       'it is a tall Victorian building which appears to be the town hall. All the windows are '
                       'smashed.')
        directions = [
            TownSquareNorthEast, None, None, None, TownSquareSouthEast, TownSquareSouth, TownSquareCentre,
            TownSquareNorth
        ]
        items = [CobbledGround(dictionary), LionStatue(dictionary)]
        super(TownSquareEast, self).__init__(name, description, directions, items)


class TownSquareSouthEast(Location):
    def __init__(self, dictionary):
        name = 'South-east corner of town square'
        description = 'You are in the south-east corner of a square. Streets leave the square to the south and east.'
        directions = [TownSquareEast, None, None, None, None, None, TownSquareSouth, TownSquareCentre]
        items = [CobbledGround(dictionary)]
        super(TownSquareSouthEast, self).__init__(name, description, directions, items)


class TownSquareSouth(Location):
    def __init__(self, dictionary):
        name = 'South side of town square'
        description = ('You are on the south side of a square. To the south is an office block with boarded up '
                       'doors and windows.')
        directions = [
            TownSquareCentre, TownSquareEast, TownSquareSouthEast, None,
            'There doesn\'t seem to be an easy way into the building.', MuseumStreetNorth, TownSquareSouthWest,
            TownSquareWest
        ]
        items = [CobbledGround(dictionary)]
        super(TownSquareSouth, self).__init__(name, description, directions, items)


class TownSquareSouthWest(Location):
    def __init__(self, dictionary):
        name = 'South-west corner of town square'
        description = 'You are in the south-west corner of a square. Streets leave the square to the south and west.'
        directions = [TownSquareWest, TownSquareCentre, TownSquareSouth, None, MuseumStreetNorth, None, None, None]
        items = [CobbledGround(dictionary)]
        super(TownSquareSouthWest, self).__init__(name, description, directions, items)


class TownSquareWest(Location):
    def __init__(self, dictionary):
        name = 'West side of town square'
        description = ('You are at the western end of a square. To the west is a building with smashed windows that '
                       'appears to be a pub. A sign hanging above the door proclaims the pub\'s name as The '
                       'Standing Order.')
        directions = [
            TownSquareNorthWest, TownSquareNorth, TownSquareCentre, TownSquareSouth, TownSquareSouthWest, None, None,
            None
        ]
        items = [CobbledGround(dictionary)]
        super(TownSquareWest, self).__init__(name, description, directions, items)


class TownSquareNorthWest(Location):
    def __init__(self, dictionary):
        name = 'North-west corner of town square'
        description = 'You are in the north-west corner of a square. Streets leave the square to the north and west.'
        directions = [None, None, TownSquareNorth, TownSquareCentre, TownSquareWest, None, None, None]
        items = [CobbledGround(dictionary)]
        super(TownSquareNorthWest, self).__init__(name, description, directions, items)


class MuseumStreetNorth(Location):
    def __init__(self, dictionary):
        name = 'North end of Museum Street'
        description = ('You are standing at the north end of a street. To the west is a large museum. On the east side '
                       'of the street is a boarded up office building. To the north is a large square.')
        directions = [
            TownSquareSouthWest, TownSquareSouth, 'There doesn\'t seem to be an easy way into the building.',
            None, None, None, None, None]
        items = [TarmacGround(dictionary)]
        super(MuseumStreetNorth, self).__init__(name, description, directions, items)


_location_class_list = [TownSquareCentre, TownSquareNorth, TownSquareNorthEast, TownSquareEast, TownSquareSouthEast,
                        TownSquareSouth, TownSquareSouthWest, TownSquareWest, TownSquareNorthWest, MuseumStreetNorth]
_start_location_class = TownSquareCentre


def build_map(dictionary, start_location=_start_location_class):
    locations = {}
    for location_class in _location_class_list:
        locations[location_class] = location_class(dictionary)
    for key, location in locations.items():
        for direction, target in location.directions_classes.items():
            if isinstance(target, type):
                location.directions[direction] = locations[target]
            elif isinstance(target, str):
                location.directions[direction] = target
    return locations[start_location]
