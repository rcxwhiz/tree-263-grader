import sys

import helper_tools


def py_grader(prob):
	print(f'Grading py problem {prob}')
	python_files = helper_tools.files.get_files(prob, 'py')
	run_files = []
	for file in python_files:
		student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
		source_file = open(file, 'r').read()
		run_files.append({'name': student_name, 'source': source_file})


def xlsx_grader(prob):
	print(f'Grading xlsx problem {prob}')


if __name__ == '__main__':
	helper_tools.input.validate_args(sys.argv)
	if sys.argv[2] == 'py':
		py_grader(sys.argv[3])
	if sys.argv[2] == 'xlsx':
		xlsx_grader(sys.argv[3])
