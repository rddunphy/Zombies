from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

NL = '\n'
BOLD = '\u001b[1m'
GREEN = '\u001b[32m'
BLUE = '\u001b[34m'
RED = '\u001b[31m'
YELLOW = '\u001b[33m'
RESET = '\u001b[0m'
PROMPT = '> '

style = style_from_dict({Token.Pound: '#006fb8', Token.Toolbar: '#ffffff bg:#333333'})

completer = WordCompleter(['look', 'go', 'hit'], ignore_case=True)

history = InMemoryHistory()


def get_toolbar(ctx):
    if ctx:
        status = ' Health: {} '.format(ctx.health)
    else:
        status = ''
    def get_bottom_toolbar_tokens(cli):
        return [(Token.Toolbar, status)]
    return get_bottom_toolbar_tokens


def get_prompt_tokens(cli):
    return [(Token.Pound, PROMPT)]


class Console:
    def __init__(self, plaintext):
        self.plaintext = plaintext
        if plaintext:
            self.prompter = NL + PROMPT
        else:
            self.prompter = NL + BLUE + PROMPT + GREEN

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

    def get_input(self, ctx):
        self.empty_line()
        if ctx:
            s = prompt(get_prompt_tokens=get_prompt_tokens, get_bottom_toolbar_tokens=get_toolbar(ctx),
                       completer=completer, style=style, history=history).strip()
        else:
            s = prompt(get_prompt_tokens=get_prompt_tokens, get_bottom_toolbar_tokens=get_toolbar(ctx),
                       completer=completer, style=style).strip()
        if len(s) > 0:
            return s
        return self.get_input(ctx)

    @staticmethod
    def empty_line():
        print('')
