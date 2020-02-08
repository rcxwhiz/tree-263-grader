import sys


def exit_msg(msg):
	print(msg)
	input('Press any key to exit...')
	sys.exit()


def validate_args(args):
	if len(args) != 3:
		exit_msg('Arguments should be [py/xlsx] [prob num]')
	if args[1] != 'py' and args[1] != 'xlsx':
		exit_msg('Only py and xlsx file formats are supported')
