import argparse
import random


class Context:

	def __init__(self, name):
		self.name = name
		self.health = 100


class Command:

	def __init__(self, verb):
		self.verb = verb


VERBS = {
	'HELP' : ['help'],
	'HIT' : ['hit', 'punch'],
	'LOOK' : ['look', 'examine', 'inspect', 'l'],
	'MOVE' : ['go', 'walk', 'move'],
	'QUIT' : ['exit', 'quit', 'q']
}


VERB_ALIASES = {}

for verb in VERBS:
	for alias in VERBS[verb]:
		VERB_ALIASES[alias] = verb


def parse(s):
	tokens = s.lower().split()
	verb = tokens[0]
	if verb in VERB_ALIASES:
		return Command(VERB_ALIASES[verb])
	return Command(verb)


def quit(ctx):
	print('Thanks for playing, {}.'.format(ctx.name))
	exit(0)


def look(ctx):
	print('You see a zombie. It looks hungry.')


def move(ctx):
	print('Moving...')
	look(ctx)


def hit(ctx):
	print('You punch the zombie. The zombie snarls and takes a bite out of you.')
	damage = random.randint(20, 30)
	ctx.health -= damage
	print('[damage: {}, health: {}]'.format(damage, ctx.health))


def help(ctx):
	print('Try entering a verb followed by an object.')


def execute(cmd, ctx):
	if cmd.verb == 'QUIT':
		quit(ctx)
	elif cmd.verb == 'LOOK':
		look(ctx)
	elif cmd.verb == 'MOVE':
		move(ctx)
	elif cmd.verb == 'HIT':
		hit(ctx)
	elif cmd.verb == 'HELP':
		help(ctx)
	else:
		print('I don\'t recognise the verb "' + cmd.verb + '".')


def get_input():
	s = input('> ').strip()
	if (len(s) > 0):
		return s
	return get_input()


def intro(ctx):
	print('You wake up with a headache.')
	look(ctx)


def game_over(ctx):
	print('{}, you are now a zombie.'.format(ctx.name))
	print('Enjoy your afterlife!')
	print('**** GAME OVER ****')
	exit(0)


def repl(ctx):
	s = get_input()
	cmd = parse(s)
	execute(cmd, ctx)
	if ctx.health <= 0:
		game_over(ctx)
	else:
		repl(ctx)


def run():
	parser = argparse.ArgumentParser(description='A zombie game.')
	parser.add_argument('-n', '--name', type=str, nargs='+', help='your name')
	args = parser.parse_args()
	if args.name:
		name = ' '.join(args.name)
		print('Hello, {}!'.format(name))
	else:
		print('Hello, future zombie!')
		print('Please enter your name.')
		name = get_input()
		print('Hi, {}!'.format(name))
	ctx = Context(name)
	intro(ctx)
	repl(ctx)


if __name__ == '__main__':
	run()
