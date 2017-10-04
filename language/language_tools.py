from nltk.corpus import cmudict

from language.words import Object


def list_of_words(tokens):
    if len(tokens) > 1:
        return '{} and {}'.format(', '.join(tokens[:-1]), tokens[-1])
    return tokens[0]


def capitalise_first_letter(token):
    return token[0].upper() + token[1:]


def add_indefinite_article(dictionary, phrase):
    tokens = phrase.split()
    return '{} {}'.format(get_indefinite_article(dictionary, tokens[0]), phrase)


def get_indefinite_article(dictionary, token):
    if dictionary.entries[token].vowel_sound_cached:
        if dictionary.entries[token].vowel_sound:
            return 'an'
        else:
            return 'a'
    else:
        for syllables in cmudict.dict().get(token, []):
            if syllables[0][-1].isdigit():
                dictionary.entries[token].vowel_sound_cached = True
                dictionary.entries[token].vowel_sound = True
                return 'an'
            else:
                dictionary.entries[token].vowel_sound_cached = True
                dictionary.entries[token].vowel_sound = False
                return 'a'


def synonyms(dictionary, token1, token2):
    return token1 in dictionary and token2 in dictionary and dictionary.get(token1) == dictionary.get(token2)


def build_object(dictionary, phrase):
    tokens = phrase.split()
    noun = dictionary.get(tokens[-1])
    adjectives = [dictionary.get(adj) for adj in tokens[:-1]]
    return Object(noun, adjectives=set(adjectives))
