
NL = '\n'
BOLD = '\u001b[1m'
GREEN = '\u001b[32m'
BLUE = '\u001b[34m'
RED = '\u001b[31m'
YELLOW = '\u001b[33m'
RESET = '\u001b[0m'
PROMPT = '> '


class Console:
    def __init__(self, plaintext):
        self.plaintext = plaintext
        if plaintext:
            self.prompt = NL + PROMPT
        else:
            self.prompt = NL + BLUE + PROMPT + GREEN

    def print_info(self, info):
        if self.plaintext:
            print(NL + '[' + info + ']')
        else:
            print(NL + YELLOW + info)

    def format_title(self, title):
        if self.plaintext:
            return '### ' + title + ' ###'
        else:
            return BOLD + title + RESET

    def format_stats(self, stats):
        if self.plaintext:
            lines = ['']
            lines.extend(['[' + stat + ']' for stat in stats])
        else:
            lines = [RED]
            lines.extend(['\t' + stat for stat in stats])
            lines[len(lines) - 1] += RESET
        return lines

    def print_block(self, block, title=None, stats=None):
        if self.plaintext:
            lines = ['']
        else:
            lines = [RESET]
        if title:
            lines.append(self.format_title(title))
        if isinstance(block, list):
            lines.extend(block)
        else:
            lines.append(block)
        if stats:
            lines.extend(self.format_stats(stats))
        print(NL.join(lines))

    def get_input(self):
        s = input(self.prompt).strip()
        if len(s) > 0:
            return s
        return self.get_input()

    @staticmethod
    def empty_line():
        print('')
