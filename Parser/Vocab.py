from Game.Executor import help_, hit, look, move, exit_, take, inventory, give, drop
from Map.Direction import Direction
from Parser.Word import Noun, DirectionWord, Adjective, Article
from Parser.Word import Verb


WORDS = {
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

    DirectionWord('north', Direction.NORTH),
    DirectionWord('south', Direction.SOUTH),
    DirectionWord('east', Direction.EAST),
    DirectionWord('west', Direction.WEST),
    DirectionWord('up', Direction.UP, aliases=['upstairs']),
    DirectionWord('down', Direction.DOWN, aliases=['downstairs']),

    Adjective('wooden'),
    Adjective('big', aliases=['large', 'huge']),
    Adjective('dead', aliases=['deceased']),

    Article('a', aliases=['an']),
    Article('the'),
} # with using and
