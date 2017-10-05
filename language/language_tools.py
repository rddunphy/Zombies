from nltk.corpus import cmudict


def list_of_words(tokens):
    if len(tokens) > 1:
        return '{} and {}'.format(', '.join(tokens[:-1]), tokens[-1])
    return tokens[0]


def capitalise_first_letter(token):
    return token[0].upper() + token[1:]


def add_indefinite_article(dictionary, phrase):
    tokens = tokenise(dictionary, phrase)
    return '{} {}'.format(get_indefinite_article(dictionary, tokens[0]), phrase)


def get_indefinite_article(dictionary, token):
    if dictionary.entries[token].vowel_sound_cached:
        if dictionary.entries[token].vowel_sound:
            return 'an'
        else:
            return 'a'
    else:
        cmu_token = token.split()[0]
        for syllables in cmudict.dict().get(cmu_token, []):
            if syllables[0][-1].isdigit():
                dictionary.entries[token].vowel_sound_cached = True
                dictionary.entries[token].vowel_sound = True
                return 'an'
            else:
                dictionary.entries[token].vowel_sound_cached = True
                dictionary.entries[token].vowel_sound = False
                return 'a'
    return 'a'


def synonyms(dictionary, token1, token2):
    return token1 in dictionary and token2 in dictionary and dictionary.get(token1) == dictionary.get(token2)


def tokenise(dictionary, phrase):
    space_separated = phrase.split()
    tokens = []
    while space_separated:
        n = len(space_separated)
        for i in range(n):
            word = ' '.join(space_separated[:n-i])
            if word in dictionary or i == n-1:
                tokens.append(word)
                space_separated = space_separated[n-i:]
                break
    return tokens
