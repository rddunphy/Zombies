from Parser.Command import Command


VERBS = {
    'HELP': ['help'],
    'HIT': ['hit', 'punch'],
    'LOOK': ['look', 'examine', 'inspect', 'l'],
    'MOVE': ['go', 'walk', 'move'],
    'EXIT': ['exit', 'quit', 'q']
}


class Parser:

    def __init__(self):
        self.verb_aliases = {}
        self.build_dict()

    def build_dict(self):
        for verb in VERBS:
            for alias in VERBS[verb]:
                self.verb_aliases[alias] = verb

    def parse(self, s):
        tokens = s.lower().split()
        verb = tokens[0]
        object_ = None
        if len(tokens) > 1:
            object_ = tokens[1]
        if verb in self.verb_aliases:
            return Command(self.verb_aliases[verb], object_)
        return Command(verb, object_)