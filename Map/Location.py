from Map.Agent import Agent
from Parser.language_tools import list_of_words, add_indefinite_article, capitalise_first_letter


class Location:

    def __init__(self, name, description, directions, items=None):
        self.name = name
        self.description = description
        self.directions = directions
        if items:
            self.items = items
        else:
            self.items = []

    def get_description(self, ctx):
        sentences = [self.description]
        things = [item for item in self.items if not isinstance(item, Agent)]
        agents = [item for item in self.items if isinstance(item, Agent)]
        if things:
            s = list_of_words([add_indefinite_article(ctx.dictionary, str(item)) for item in things])
            verb = 'is'
            if len(things) > 1:
                verb = 'are'
            sentences.append('{} {} lying on the ground.'.format(capitalise_first_letter(s), verb))
        if agents:
            s = list_of_words([add_indefinite_article(ctx.dictionary, str(agent)) for agent in agents])
            sentences.append('You see {}.'.format(s))
        return ' '.join(sentences)
