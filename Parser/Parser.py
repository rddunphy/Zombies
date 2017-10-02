from Parser.Command import Command


VERBS = {
    'HELP': ['help'],
    'HIT': ['hit', 'punch'],
    'LOOK': ['look', 'examine', 'inspect'],
    'MOVE': ['go', 'walk', 'move'],
    'EXIT': ['exit', 'quit'],
    'TAKE': ['take'],
    'INVENTORY': ['inventory']
}


def is_valid_object(ctx, object_):
    return not object_ or object_ in ctx.available_items() or object_ in {'north', 'south', 'east', 'west'}


class Parser:

    def __init__(self):
        self.verb_aliases = {}
        self.build_dict()

    def build_dict(self):
        for verb in VERBS:
            for alias in VERBS[verb]:
                self.verb_aliases[alias] = verb

    def parse(self, s, ctx):
        tokens = s.lower().split()
        verb = tokens[0]
        object_ = None
        if len(tokens) > 1:
            object_ = tokens[1]
        if verb in self.verb_aliases and is_valid_object(ctx, object_):
            ctx.known_words.add(verb)
            if object_:
                ctx.known_words.add(object_)
            return Command(self.verb_aliases[verb], object_)
        return Command(verb, object_)
