from Map.Agent import Agent
from Map.Direction import Direction
from Map.Item import Item
from Map.Location import Location
from Map.Zombie import Zombie
from Parser.Dictionary import Dictionary
from Parser.Object import Object


class Map:
    def __init__(self):
        dictionary = Dictionary()
        self.locations = {
            0: Location("Centre of square",
                        'You are in the centre of a large square. There is a wooden board on the ground next to you.',
                        {Direction.NORTH: 1, Direction.SOUTH: 2, Direction.EAST: 3, Direction.WEST: 4},
                        items=[Item('It\'s a fairly plain but sturdy plank of wood.',
                                    Object(dictionary.nouns['board'], adjectives={dictionary.adjectives['wooden']}))]),
            1: Location("North side of square", 'You are on the north side of the square. You see a zombie.',
                        {Direction.SOUTH: 0, Direction.EAST: 3, Direction.WEST: 4},
                        items=[Zombie(
                            'The cross-eyed zombie seems to be ignoring you. He appears to have been a banker.',
                                    Object(dictionary.nouns['zombie']))]),
            2: Location("South side of square", 'You are on the south side of the square. There are buildings.',
                        {Direction.NORTH: 0, Direction.EAST: 3, Direction.WEST: 4}),
            3: Location("East side of square", 'You are on the east side of the square. There are buildings.',
                        {Direction.WEST: 0, Direction.NORTH: 1, Direction.SOUTH: 2}),
            4: Location("West side of square", 'You are on the west side of the square. There are buildings.',
                        {Direction.EAST: 0, Direction.NORTH: 1, Direction.SOUTH: 2})
        }
