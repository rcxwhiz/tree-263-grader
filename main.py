import sys

import helper_tools


def py_grader(prob):
	print(f'Grading py problem {prob}')


def xlsx_grader(prob):
	print(f'Grading xlsx problem {prob}')


if __name__ == '__main__':
	helper_tools.input.validate_args(sys.argv)
	if sys.argv[2] == 'py':
		py_grader(sys.argv[3])
	if sys.argv[2] == 'xlsx':
		xlsx_grader(sys.argv[3])
