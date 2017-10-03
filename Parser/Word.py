
class Word:

    def __init__(self, token, aliases=None):
        self.token = token
        if aliases:
            self.aliases = aliases
        else:
            self.aliases = []

    def __str__(self):
        return self.token

    def __repr__(self):
        return '\'' + self.token + '\''


class Verb(Word):

    def __init__(self, token, fn, aliases=None, direct_required=False, indirect_required=False, direction_required=False, elementary=False):
        super(Verb, self).__init__(token, aliases=aliases)
        self.fn = fn
        self.direct_required = direct_required
        self.indirect_required = indirect_required
        self.direction_required = direction_required
        self.elementary = elementary


class Noun(Word):

    def __init__(self, token, aliases=None, plurals=None):
        super(Noun, self).__init__(token, aliases=aliases)
        if plurals:
            self.plurals = plurals
        else:
            self.plurals = []
