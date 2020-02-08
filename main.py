import os
import sys
import numpy as np
import matplotlib

import helper_tools


def run_file(file_name, out_file):
	temp = sys.stdout
	sys.stdout = open(out_file, 'w')
	try:
		exec(open(file_name).read())
		sys.stdout = temp
		return open(out_file, 'r').read()
	except Exception:
		print(f'Could not read {file_name}')
		sys.stdout = temp
		return 'COULD NOT READ'


def py_grader(prob):
	print(f'Grading py problem {prob}')
	python_files = helper_tools.files.get_files(prob, 'py')
	run_files = []
	for file in python_files:
		temp_out = 'TEMP_OUPUT_JOSH_GRADER.txt'
		student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
		source_file = open(file, 'r').read()

		run_files.append({'name': student_name, 'source': source_file, 'out': run_file(file, temp_out)})

	bad_reads = 0
	for student in run_files:
		if student['out'] is None:
			bad_reads += 1
	print(f'There were {bad_reads} bad reads')


def xlsx_grader(prob):
	print(f'Grading xlsx problem {prob}')


if __name__ == '__main__':
	helper_tools.input.validate_args(sys.argv)
	if sys.argv[2] == 'py':
		py_grader(sys.argv[3])
	if sys.argv[2] == 'xlsx':
		xlsx_grader(sys.argv[3])
