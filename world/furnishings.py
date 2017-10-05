import math

from world.items import Item


class Furnishing(Item):
    def __init__(self, name, description, nouns, short_name=None, adjectives=None):
        super(Furnishing, self).__init__(name, description, math.inf, nouns, short_name=short_name,
                                         adjectives=adjectives)


class Ground(Furnishing):
    def __init__(self, dictionary, name, description, nouns, adjectives=None, short_name='ground'):
        if not nouns:
            nouns = set()
        nouns.add(dictionary.get('ground'))
        super(Ground, self).__init__(name, description, nouns, adjectives=adjectives, short_name=short_name)


class CobbledGround(Ground):
    def __init__(self, dictionary):
        nouns = {dictionary.get('cobbles')}
        adjectives = {dictionary.get('cobbled')}
        description = 'It\'s the ground. It looks pretty solid.'
        name = 'cobbles'
        super(CobbledGround, self).__init__(dictionary, name, description, nouns, adjectives=adjectives)


class TarmacGround(Ground):
    def __init__(self, dictionary):
        nouns = {dictionary.get('road'), dictionary.get('tarmac')}
        description = 'It\'s the ground. It looks pretty solid.'
        name = 'road'
        super(TarmacGround, self).__init__(dictionary, name, description, nouns)


class Statue(Furnishing):
    def __init__(self, dictionary, name, description, nouns, adjectives=None, short_name='statue'):
        if not nouns:
            nouns = set()
        nouns.add(dictionary.get('statue'))
        super(Statue, self).__init__(name, description, nouns, adjectives=adjectives, short_name=short_name)


class LionStatue(Statue):
    def __init__(self, dictionary):
        name = 'lion statue'
        description = 'It\'s a marble statue of a lion on top of a rectangular base. It\'s a good twelve feet long.'
        nouns = {dictionary.get('lion'), dictionary.get('lion statue')}
        adjectives = {dictionary.get('large')}
        super(LionStatue, self).__init__(dictionary, name, description, nouns, adjectives=adjectives)
