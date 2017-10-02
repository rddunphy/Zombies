from Parser.Word import Word


class Verb(Word):

    def __init__(self, token, fn, aliases=[], direct_required=False, indirect_required=False, elementary=False):
        super(Verb, self).__init__(token, aliases=aliases)
        self.fn = fn
        self.direct_required = direct_required
        self.indirect_required = indirect_required
        self.elementary = elementary
