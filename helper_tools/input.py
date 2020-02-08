import os
import sys

supported_files = ['py', 'xlsx']
hw_directory = r'C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA'


def exit_msg(msg):
	print('[ERROR]')
	print(msg)
	input('Press any key to exit...')
	sys.exit()


def validate_args(args):
	if len(args) != 4:
		exit_msg(f'Arguments should be [hw num] [{"/".join(supported_files)}] [prob num]')
	if args[2] not in supported_files:
		exit_msg(f'File formats supported: {" ".join(supported_files)}')
	try:
		os.chdir(os.path.join(hw_directory, 'HW ' + args[1]))
	except FileNotFoundError:
		exit_msg(f'Could not find the HW folder:\n'
		         f'{os.path.join(hw_directory, "HW " + args[1])}')
	hw_dirs = os.listdir('.')
	for cdir in hw_dirs:
		if 'Gradebook Bundled Download' in cdir:
			os.chdir(cdir)
			print(f'Finding hw files in:\n'
			      f'{os.getcwd()}')
			return None
	exit_msg(f'Unable to find a Gradebook Bundled Download folder in:\n'
	         f'{os.getcwd()}')
