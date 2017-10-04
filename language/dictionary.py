from game.actions import help_, hit, look, move, exit_, take, inventory, give, drop
from world.locations import Direction
from language.words import Noun, DirectionWord, Adjective, Article, Preposition, Conjunction
from language.words import Verb


class DictionaryEntry:
    def __init__(self, word, is_plural=False, vowel_sound_cached=False, vowel_sound=False):
        self.word = word
        self.is_plural = is_plural
        self.vowel_sound_cached = vowel_sound_cached
        self.vowel_sound = vowel_sound


class Dictionary:
    def __init__(self):
        self.entries = {}
        self.build()

    def build(self):
        for word in VOCABULARY:
            self.entries[word.token] = DictionaryEntry(word)
            for alias in word.aliases:
                self.entries[alias] = DictionaryEntry(word)
            if hasattr(word, 'plurals'):
                for plural in word.plurals:
                    self.entries[plural] = DictionaryEntry(word, is_plural=True)

    def get(self, token):
        if token in self:
            return self.entries[token].word
        return None

    def is_plural(self, token):
        if token in self:
            return self.entries[token].is_plural
        return False

    def __contains__(self, item):
        return item in self.entries


VOCABULARY = {
    Verb('help', help_, aliases=['help me', 'show help'], elementary=True),
    Verb('hit', hit, aliases=['punch', 'attack', 'kill'], direct_required=True),
    Verb('look', look, aliases=['look around'], elementary=True),
    Verb('look at', look, aliases=['examine', 'inspect'], direct_required=True),
    Verb('move', move, aliases=['go', 'walk', 'go to'], direction_required=True),
    Verb('run', move, aliases=['run away', 'flee', 'sprint', 'escape'], direction_required=True),
    Verb('exit', exit_, aliases=['quit'], elementary=True),
    Verb('take', take, aliases=['pick up', 'lift'], direct_required=True),
    Verb('drop', drop, aliases=['put down'], direct_required=True),
    Verb('give', give, direct_required=True, indirect_required=True),
    Verb('inventory', inventory, aliases=['show inventory'], elementary=True),

    Noun('zombie', plurals=['zombies']),
    Noun('board', aliases=['plank'], plurals=['boards, planks']),

    DirectionWord('north', Direction.N, aliases=['n']),
    DirectionWord('north-east', Direction.NE, aliases=['northeast', 'north east', 'ne']),
    DirectionWord('east', Direction.E, aliases=['e']),
    DirectionWord('south-east', Direction.SE, aliases=['southeast', 'south east', 'se']),
    DirectionWord('south', Direction.S, aliases=['s']),
    DirectionWord('south-west', Direction.SW, aliases=['southwest', 'south west', 'sw']),
    DirectionWord('west', Direction.W, aliases=['w']),
    DirectionWord('north-west', Direction.NW, aliases=['northwest', 'north west', 'nw']),
    DirectionWord('up', Direction.UP, aliases=['upstairs']),
    DirectionWord('down', Direction.DN, aliases=['downstairs']),

    Adjective('wooden'),
    Adjective('big', aliases=['large', 'huge']),
    Adjective('dead', aliases=['deceased']),
    Adjective('fat', aliases=['obese']),
    Adjective('cross-eyed'),

    Article('a', aliases=['an']),
    Article('the'),

    Preposition('with', aliases=['using']),
    Preposition('to'),

    Conjunction('and')
}
