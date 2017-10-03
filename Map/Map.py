from Map.Direction import Direction
from Map.Item import Item
from Map.Location import Location
from Map.Zombie import Zombie
from Parser.Object import Object


class Map:

    def __init__(self, dictionary):
        self.locations = {
            0: Location("Centre of square",
                        'You are in the centre of a large square.',
                        {Direction.NORTH: 1, Direction.SOUTH: 2, Direction.EAST: 3, Direction.WEST: 4},
                        items=[Item('It\'s a fairly plain but sturdy plank of wood.',
                                    Object(dictionary.get('board'), adjectives={dictionary.get('wooden')}), 3)]),
            1: Location("North side of square", 'You are on the north side of the square.',
                        {Direction.SOUTH: 0, Direction.EAST: 3, Direction.WEST: 4},
                        items=[Zombie(
                            'The cross-eyed zombie is ignoring you. He appears to have been a fat banker at one '
                            'point, but is now only interested in the handful of brains he is currently nibbling on.',
                            'The zombie is lying on the ground in pieces. A maggot is crawling out of its left ear.',
                            Object(dictionary.get('zombie')), 95)]),
            2: Location("South side of square", 'You are on the south side of the square. There are buildings.',
                        {Direction.NORTH: 0, Direction.EAST: 3, Direction.WEST: 4}),
            3: Location("East side of square", 'You are on the east side of the square. There are buildings.',
                        {Direction.WEST: 0, Direction.NORTH: 1, Direction.SOUTH: 2}),
            4: Location("West side of square", 'You are on the west side of the square. There are buildings.',
                        {Direction.EAST: 0, Direction.NORTH: 1, Direction.SOUTH: 2})
        }
