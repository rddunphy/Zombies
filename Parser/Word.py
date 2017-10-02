
class Word:

    def __init__(self, token, aliases=[]):
        self.token = token
        self.aliases = aliases

    def __repr__(self):
        return '\'' + self.token + '\''
