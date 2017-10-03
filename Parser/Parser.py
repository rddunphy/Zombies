from Parser.Command import Command
from Parser.Dictionary import Dictionary
from Parser.Object import Object


def is_valid_object(ctx, object_):
    return not object_ or object_ in ctx.available_items() or object_ in {'north', 'south', 'east', 'west'}


class ParseError(Exception):
    pass


class Parser:

    def __init__(self):
        self.dictionary = Dictionary()

    def parse_verb(self, tokens):
        verb = None
        if len(tokens) > 1:
            first_two_words = tokens[0] + ' ' + tokens[1]
            if first_two_words in self.dictionary.verbs:
                verb = self.dictionary.verbs[first_two_words]
                tokens = tokens[2:]
        if not verb and tokens[0] in self.dictionary.verbs:
            verb = self.dictionary.verbs[tokens[0]]
            tokens = tokens[1:]
        if not verb:
            raise ParseError('I do not recognise {} as a verb.'.format(tokens[0]))
        if verb.elementary and tokens:
            raise ParseError('I can\'t {} things.'.format(verb.token))
        return verb, tokens

    def parse_object(self, tokens):
        if tokens and (tokens[0] == 'a' or tokens[0] == 'the'):
            tokens = tokens[1:]
        if not tokens or tokens[0] == 'and':
            return None, tokens
        adjectives = set()
        while tokens:
            t = tokens[0]
            tokens = tokens[1:]
            if t in self.dictionary.adjectives:
                adjectives.add(self.dictionary.adjectives[t])
            elif t in self.dictionary.nouns:
                noun = self.dictionary.nouns[t]
                return Object(noun, adjectives=adjectives), tokens
            elif t in self.dictionary.plural_nouns:
                noun = self.dictionary.plural_nouns[t]
                return Object(noun, plural=True, adjectives=adjectives), tokens
            else:
                raise ParseError('I don\'t recognise {} as a noun.'.format(t))
        raise ParseError('I expect a noun after this adjective.')

    def parse_direction(self, tokens):
        if tokens and tokens[0] in self.dictionary.directions:
            return self.dictionary.directions[tokens[0]], tokens[1:]
        else:
            raise ParseError('Direction expected.')

    def parse(self, s, ctx, tokens=None):
        if not tokens:
            tokens = s.lower().split()
        verb, tokens = self.parse_verb(tokens)
        if verb.direction_required:
            direction, tokens = self.parse_direction(tokens)
            cmd = Command(verb, direction=direction)
        else:
            direct, tokens = self.parse_object(tokens)
            if tokens and tokens[0] == 'to':
                tokens = tokens[1:]
                if not tokens:
                    raise ParseError('{} to what?'.format(verb.token))
                indirect = direct
                direct, tokens = self.parse_object(tokens)
            else:
                indirect, tokens = self.parse_object(tokens)
            if verb.direct_required and not direct:
                raise ParseError('{} requires a direct object'.format(verb.token))
            if verb.indirect_required and not indirect:
                raise ParseError('{} requires an indirect object'.format(verb.token))
            cmd = Command(verb, direct=direct, indirect=indirect)
        if tokens and tokens[0] == 'and':
            return [cmd] + self.parse(s, ctx, tokens=tokens[1:])
        if tokens:
            raise ParseError('Leftover tokens: {}'.format(' '.join(tokens)))
        ctx.known_words.update(s.lower().split())
        return [cmd]
