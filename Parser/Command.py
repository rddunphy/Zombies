class Command:
    
    def __init__(self, verb, direct=None, indirect=None, using=None):
        self.verb = verb
        self.direct = direct
        self.indirect = indirect
        self.using = using
