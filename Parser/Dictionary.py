from Parser.Vocab import WORDS


class DictionaryEntry:

    def __init__(self, word, is_plural=False, vowel_sound_cached=False, vowel_sound=False):
        self.word = word
        self.is_plural = is_plural
        self.vowel_sound_cached = vowel_sound_cached
        self.vowel_sound = vowel_sound


class Dictionary:

    def __init__(self):
        self.entries = {}
        self.build()

    def build(self):
        for word in WORDS:
            self.entries[word.token] = DictionaryEntry(word)
            for alias in word.aliases:
                self.entries[alias] = DictionaryEntry(word)
            if hasattr(word, 'plurals'):
                for plural in word.plurals:
                    self.entries[plural] = DictionaryEntry(word, is_plural=True)

    def get(self, token):
        if token in self:
            return self.entries[token].word
        return None

    def is_plural(self, token):
        if token in self:
            return self.entries[token].is_plural
        return False

    def __contains__(self, item):
        return item in self.entries
