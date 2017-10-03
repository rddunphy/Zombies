from Parser.Command import Command
from Parser.Object import Object
from Parser.Word import Verb, Article, Noun, Adjective, DirectionWord, Conjunction
from Parser.language_tools import capitalise_first_letter


class ParseError(Exception):
    pass


class Parser:

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def parse_verb(self, tokens):
        if len(tokens) > 1:
            first_two_tokens = '{} {}'.format(tokens[0], tokens[1])
            if isinstance(self.dictionary.get(first_two_tokens), Verb):
                return self.dictionary.get(first_two_tokens), tokens[2:]
        token = tokens[0]
        if isinstance(self.dictionary.get(token), Verb):
            return self.dictionary.get(token), tokens[1:]
        raise ParseError('I do not recognise {} as a verb.'.format(token))

    def parse_object(self, tokens):
        if not tokens:
            return None, tokens
        word = self.dictionary.get(tokens[0])
        if isinstance(word, Article):
            tokens = tokens[1:]
            if not tokens:
                raise ParseError('Article should be followed by a noun phrase.')
            word = self.dictionary.get(tokens[0])
        if not isinstance(word, Noun) and not isinstance(word, Adjective):
            return None, tokens
        adjectives = set()
        while tokens:
            token = tokens[0]
            word = self.dictionary.get(token)
            tokens = tokens[1:]
            if isinstance(word, Adjective):
                adjectives.add(word)
            elif isinstance(word, Noun):
                return Object(word, plural=self.dictionary.is_plural(token), adjectives=adjectives), tokens
            else:
                raise ParseError('I don\'t recognise {} as a noun.'.format(token))
        raise ParseError('I expect a noun after this adjective.')

    def parse_direction(self, tokens):
        if tokens and isinstance(self.dictionary.get(tokens[0]), DirectionWord):
            return self.dictionary.get(tokens[0]).direction, tokens[1:]
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
            indirect = None
            if tokens and tokens[0] == 'to':
                tokens = tokens[1:]
                if not tokens:
                    raise ParseError('{} to what?'.format(capitalise_first_letter(str(verb))))
                indirect, tokens = self.parse_object(tokens)
            else:
                obj2, tokens = self.parse_object(tokens)
                if obj2:
                    indirect = direct
                    direct = obj2
            using = None
            if tokens and (tokens[0] == 'with' or tokens[0] == 'using'):
                tokens = tokens[1:]
                if not tokens:
                    raise ParseError('{} using what?'.format(capitalise_first_letter(str(verb))))
                using, tokens = self.parse_object(tokens)
            if verb.direct_required and not direct:
                raise ParseError('{} requires a direct object'.format(capitalise_first_letter(str(verb))))
            if verb.indirect_required and not indirect:
                raise ParseError('{} requires an indirect object'.format(capitalise_first_letter(str(verb))))
            if verb.elementary and (direct or indirect or using):
                raise ParseError('I can\'t {} things.'.format(verb.token))
            cmd = Command(verb, direct=direct, indirect=indirect, using=using)
        if tokens and isinstance(self.dictionary.get(tokens[0]), Conjunction):
            return [cmd] + self.parse(s, ctx, tokens=tokens[1:])
        if tokens:
            raise ParseError('Leftover tokens: {}'.format(' '.join(tokens)))
        ctx.known_words.update(s.lower().split())
        return [cmd]
