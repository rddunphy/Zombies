import argparse


def run():
	parser = argparse.ArgumentParser(description='A zombie game.')
	parser.add_argument('-n', '--name', type=str, nargs='+', help='your name')
	args = parser.parse_args()
	if args.name:
		name = ' '.join(args.name)
		print("Hello, {}!".format(name))
	else:
		print("Hello, future zombie!")
		print("Please enter your name.")
		name = input("> ")
		print("Hi, {}!".format(name))
	print("{}, you are now a zombie.".format(name))
	print("Enjoy your afterlife!")


if __name__ == "__main__":
	run()
