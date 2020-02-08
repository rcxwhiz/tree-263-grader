import os
import sys

import helper_tools


def py_grader(prob):
	print(f'Grading py problem {prob}')
	python_files = helper_tools.files.get_files(prob, 'py')
	run_files = []
	for file in python_files:
		temp_out = 'TEMP_OUPUT_JOSH_GRADER.txt'
		student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
		source_file = open(file, 'r').read()

		new_runner = helper_tools.files.PyRunner()
		run_files.append({'name': student_name, 'source': source_file, 'out': new_runner.RUN_FILE_WRAPPER(file, temp_out)})

	bad_reads = []
	for student in run_files:
		if student['out'] in helper_tools.files.MY_CLASS_ERROR_MESSAGES:
			bad_reads.append(student['name'])
	if len(bad_reads) == 0:
		print('There were no bad runs')
	else:
		print('Could not run:')
		for student in bad_reads:
			print(f'  {student}')


def xlsx_grader(prob):
	print(f'Grading xlsx problem {prob}')


if __name__ == '__main__':
	helper_tools.input.validate_args(sys.argv)
	if sys.argv[2] == 'py':
		py_grader(sys.argv[3])
	if sys.argv[2] == 'xlsx':
		xlsx_grader(sys.argv[3])
