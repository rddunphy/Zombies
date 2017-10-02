from Game.Executor import help_, hit, look, move, exit_, take, inventory, give
from Parser.Command import Command
from Parser.Verb import Verb
from Parser.Word import Word

VERBS = {
    Verb('help', help_, elementary=True),
    Verb('hit', hit, aliases=['punch', 'attack', 'kill'], direct_required=True),
    Verb('look', look, aliases=['look at', 'examine', 'inspect']),
    Verb('move', move, aliases=['go', 'walk', 'go to'], direct_required=True),
    Verb('exit', exit_, aliases=['quit'], elementary=True),
    Verb('take', take, aliases=['pick up'], direct_required=True),
    Verb('give', give, direct_required=True, indirect_required=True),
    Verb('inventory', inventory, elementary=True)
}


def is_valid_object(ctx, object_):
    return not object_ or object_ in ctx.available_items() or object_ in {'north', 'south', 'east', 'west'}


class Parser:

    def __init__(self):
        self.verb_aliases = {}
        self.build_dict()

    def build_dict(self):
        for verb in VERBS:
            self.verb_aliases[verb.token] = verb
            for alias in verb.aliases:
                self.verb_aliases[alias] = verb

    def parse_verb(self, tokens):
        verb = None
        if len(tokens) > 1:
            first_two_words = tokens[0] + ' ' + tokens[1]
            if first_two_words in self.verb_aliases:
                verb = self.verb_aliases[first_two_words]
                tokens = tokens[2:]
        if not verb and tokens[0] in self.verb_aliases:
            verb = self.verb_aliases[tokens[0]]
            tokens = tokens[1:]
        if not verb:
            print('I do not recognise {} as a verb.'.format(tokens[0]))
            return None, tokens
        if verb.elementary and tokens:
            print('I can\'t {} things.'.format(verb.token))
            return None, tokens
        return verb, tokens

    @staticmethod
    def parse_object(tokens):
        if not tokens:
            return None, tokens
        if tokens[0] == 'a' or tokens[0] == 'the':
            tokens = tokens[1:]
        if not tokens:
            return None, tokens
        t = tokens[0]
        tokens = tokens[1:]
        return Word(t), tokens

    def parse(self, s, ctx):
        tokens = s.lower().split()
        verb, tokens = self.parse_verb(tokens)
        if not verb:
            return None
        direct, tokens = self.parse_object(tokens)
        if tokens and tokens[0] == 'to':
            tokens = tokens[1:]
            if not tokens:
                print('{} to what?'.format(verb.token))
                return None
            indirect = direct
            direct = self.parse_object(tokens)
        else:
            indirect, tokens = self.parse_object(tokens)
        if tokens:
            print('Leftover tokens: {}'.format(' '.join(tokens)))
            return None
        if verb.direct_required and not direct:
            print('{} requires a direct object'.format(verb.token))
            return None
        if verb.indirect_required and not indirect:
            print('{} requires an indirect object'.format(verb.token))
            return None
        ctx.known_words.update(s.lower().split())
        return Command(verb, direct=direct, indirect=indirect)
