from enum import Enum

from language.language_tools import list_of_words, add_indefinite_article, capitalise_first_letter
from world.items import Item
from world.agents import Zombie, Agent
from language.words import Object


class Direction(Enum):
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'
    UP = 'up'
    DOWN = 'down'


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


class Location:

    def __init__(self, name, description, directions, items=None):
        self.name = name
        self.description = description
        self.directions = directions
        if items:
            self.items = items
        else:
            self.items = []

    def get_description(self, ctx):
        sentences = [self.description]
        things = [item for item in self.items if not isinstance(item, Agent)]
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
