from Game.Executor import help_, hit, look, move, exit_, take, inventory, give
from Map.Direction import Direction
from Parser.Word import Noun
from Parser.Word import Verb
from Parser.Word import Word

VERBS = {
    Verb('help', help_, aliases=['help me'], elementary=True),
    Verb('hit', hit, aliases=['punch', 'attack', 'kill'], direct_required=True),
    Verb('look', look, aliases=['look around'], elementary=True),
    Verb('look at', look, aliases=['examine', 'inspect'], direct_required=True),
    Verb('move', move, aliases=['go', 'walk', 'go to'], direction_required=True),
    Verb('exit', exit_, aliases=['quit'], elementary=True),
    Verb('take', take, aliases=['pick up'], direct_required=True),
    Verb('give', give, direct_required=True, indirect_required=True),
    Verb('inventory', inventory, elementary=True)
}

NOUNS = {
    Noun('zombie', plurals=['zombies']),
    Noun('board', aliases=['plank'], plurals=['boards, planks'])
}

DIRECTIONS = {
    (Word('north'), Direction.NORTH),
    (Word('south'), Direction.SOUTH),
    (Word('east'), Direction.EAST),
    (Word('west'), Direction.WEST),
    (Word('up', aliases=['upstairs']), Direction.UP),
    (Word('down', aliases=['downstairs']), Direction.DOWN)
}

ADJECTIVES = {
    Word('wooden'),
    Word('big', aliases=['large', 'huge']),
    Word('dead', aliases=['deceased'])
}
