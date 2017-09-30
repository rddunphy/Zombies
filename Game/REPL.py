import sys

from Game.Executor import execute


def get_input():
    s = input('> ').strip()
    if len(s) > 0:
        return s
    return get_input()


def intro():
    print('You wake up with a headache. In front of you is a zombie.')


def game_over(ctx):
    print('{}, you are now a zombie.'.format(ctx.name))
    print('Enjoy your afterlife!')
    print('**** GAME OVER ****')
    sys.exit(0)


def repl(parser, ctx):
    s = get_input()
    cmd = parser.parse(s)
    execute(cmd, ctx)
    if ctx.health <= 0:
        game_over(ctx)
    else:
        repl(parser, ctx)
