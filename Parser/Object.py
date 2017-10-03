

class Object:

    def __init__(self, noun, plural=False, adjectives=None):
        self.noun = noun
        self.plural = plural
        if adjectives:
            self.adjectives = adjectives
        else:
            self.adjectives = set()

    def __str__(self):
        words = list(self.adjectives) + [self.noun]
        return ' '.join([str(w) for w in words])
