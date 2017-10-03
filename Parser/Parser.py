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
                return self.dictionary.get(first_two_tokens), first_two_tokens, tokens[2:]
        token = tokens[0]
        if isinstance(self.dictionary.get(token), Verb):
            return self.dictionary.get(token), token, tokens[1:]
        raise ParseError('I do not recognise \'{}\' as a verb.'.format(token))

    def parse_object(self, tokens, verb_token):
        if not tokens:
            return None, '', tokens
        word = self.dictionary.get(tokens[0])
        if isinstance(word, Article):
            article = tokens[0]
            tokens = tokens[1:]
            if not tokens:
                raise ParseError('{} {} what?'.format(capitalise_first_letter(verb_token), article))
            word = self.dictionary.get(tokens[0])
        if not word:
            raise ParseError('I don\'t recognise \'{}\' as a noun.'.format(tokens[0]))
        if not isinstance(word, Noun) and not isinstance(word, Adjective):
            return None, '', tokens
        adjectives = set()
        while tokens:
            token = tokens[0]
            word = self.dictionary.get(token)
            tokens = tokens[1:]
            if isinstance(word, Adjective):
                adjectives.add(word)
            elif isinstance(word, Noun):
                return Object(word, plural=self.dictionary.is_plural(token), adjectives=adjectives), token, tokens
            else:
                raise ParseError('I don\'t recognise \'{}\' as a noun.'.format(token))
        raise ParseError('I expect a noun after this adjective.')

    def parse_direction(self, tokens, verb_token):
        if tokens and isinstance(self.dictionary.get(tokens[0]), DirectionWord):
            return self.dictionary.get(tokens[0]).direction, tokens[1:]
        else:
            raise ParseError('Where do you want to {}?'.format(verb_token))

    def parse(self, s, ctx, tokens=None):
        if tokens == []:
            return None
        if not tokens:
            tokens = s.lower().split()
        verb, verb_token, tokens = self.parse_verb(tokens)
        if verb.direction_required:
            direction, tokens = self.parse_direction(tokens, verb_token)
            cmd = Command(verb, direction=direction)
        else:
            direct, direct_token, tokens = self.parse_object(tokens, verb_token)
            indirect = None
            if tokens and tokens[0] == 'to':
                tokens = tokens[1:]
                if not tokens:
                    raise ParseError('{} to what?'.format(capitalise_first_letter(verb_token)))
                indirect, indirect_token, tokens = self.parse_object(tokens, verb_token)
            else:
                obj2, obj2_token, tokens = self.parse_object(tokens, verb_token)
                if obj2:
                    indirect = direct
                    direct = obj2
                    direct_token = obj2_token
            using = None
            if tokens and (tokens[0] == 'with' or tokens[0] == 'using'):
                tokens = tokens[1:]
                if not tokens:
                    raise ParseError('What do you want to {} with?'.format(verb_token))
                using, using_token, tokens = self.parse_object(tokens, verb_token)
            if verb.direct_required and not direct:
                raise ParseError('What do you want to {}?'.format(verb_token))
            if verb.indirect_required and not indirect:
                raise ParseError('What do you want to {} the {} to?'.format(verb_token, direct_token))
            if verb.elementary and (direct or indirect or using):
                raise ParseError('You can\'t {} things.'.format(verb_token))
            cmd = Command(verb, direct=direct, indirect=indirect, using=using)
        if tokens and isinstance(self.dictionary.get(tokens[0]), Conjunction):
            next_cmds = self.parse(s, ctx, tokens=tokens[1:])
            if next_cmds:
                return [cmd] + next_cmds
            else:
                return [cmd]
        if tokens:
            raise ParseError('Leftover tokens: {}'.format(' '.join(tokens)))
        ctx.known_words.update(s.lower().split())
        return [cmd]
