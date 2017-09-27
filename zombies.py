import argparse
import random


class Location:

	def __init__(self, description, directions):
		self.description = description
		self.directions = directions


class Context:

	def __init__(self, name, location):
		self.name = name
		self.health = 100
		self.location = location

	def move(self, direction):
		loc = self.location.directions[direction]
		self.location = LOCATIONS[loc]


class Command:

	def __init__(self, verb, object_):
		self.verb = verb
		self.object = object_


LOCATIONS = {
	0 : Location("Centre of square", {'north' : 1, 'south' : 2, 'east' : 3, 'west' : 4}),
	1 : Location("North side of square", {'south' : 0, 'east' : 3, 'west' : 4}),
	2 : Location("South side of square", {'north' : 0, 'east' : 3, 'west' : 4}),
	3 : Location("East side of square", {'west' : 0, 'north' : 1, 'south' : 2}),
	4 : Location("West side of square", {'east' : 0, 'north' : 1, 'south' : 2})
}


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
	object_ = None
	if len(tokens) > 1:
		object_ = tokens[1]
	if verb in VERB_ALIASES:
		return Command(VERB_ALIASES[verb], object_)
	return Command(verb, object_)


def quit(cmd, ctx):
	print('Thanks for playing, {}.'.format(ctx.name))
	exit(0)


def look(cmd, ctx):
	print(ctx.location.description)
	print('You see a zombie. It looks hungry.')


def move(cmd, ctx):
	if cmd.object == None:
		print('Where do you want to go?')
	elif cmd.object in ctx.location.directions:
		ctx.move(cmd.object)
		look(cmd, ctx)
	else:
		print('I don\'t know how to go "' + cmd.object + '"')


def hit(cmd, ctx):
	if cmd.object == None:
		print('What do you want to hit?')
	elif cmd.object == 'zombie':
		print('You punch the zombie. The zombie snarls and takes a bite out of you.')
		damage = random.randint(20, 30)
		ctx.health -= damage
		print('[damage: {}, health: {}]'.format(damage, ctx.health))
	else:
		print('I don\'t know how to hit "' + cmd.object + '".')


def help(cmd, ctx):
	if cmd.object != None and cmd.object != 'me':
		print('I don\'t know how to help "' + cmd.object + '".')
	else:
		print('Try entering a verb followed by an object.')


def execute(cmd, ctx):
	if cmd.verb == 'QUIT':
		quit(cmd, ctx)
	elif cmd.verb == 'LOOK':
		look(cmd, ctx)
	elif cmd.verb == 'MOVE':
		move(cmd, ctx)
	elif cmd.verb == 'HIT':
		hit(cmd, ctx)
	elif cmd.verb == 'HELP':
		help(cmd, ctx)
	else:
		print('I don\'t recognise the verb "' + cmd.verb + '".')


def get_input():
	s = input('> ').strip()
	if (len(s) > 0):
		return s
	return get_input()


def intro(ctx):
	print('You wake up with a headache. In front of you is a zombie.')


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
	ctx = Context(name, LOCATIONS[0])
	intro(ctx)
	repl(ctx)


if __name__ == '__main__':
	run()
