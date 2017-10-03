from Parser.Vocab import VERBS, NOUNS, ADJECTIVES, DIRECTIONS


class Dictionary:

    def __init__(self):
        self.verbs = {}
        self.nouns = {}
        self.plural_nouns = {}
        self.adjectives = {}
        self.directions = {}
        self.build()

    def build(self):
        for verb in VERBS:
            self.verbs[verb.token] = verb
            for alias in verb.aliases:
                self.verbs[alias] = verb
        for noun in NOUNS:
            self.nouns[noun.token] = noun
            for alias in noun.aliases:
                self.nouns[alias] = noun
            for plural in noun.plurals:
                self.plural_nouns[plural] = noun
        for adjective in ADJECTIVES:
            self.adjectives[adjective.token] = adjective
            for alias in adjective.aliases:
                self.adjectives[alias] = adjective
        for tuple in DIRECTIONS:
            self.directions[tuple[0].token] = tuple[1]
