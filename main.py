import os
import sys

import helper_tools


def py_grader(prob, hw):
	print(f'Grading py problem {prob}')

	temp_out = 'TEMP_OUPUT_JOSH_GRADER.txt'
	if int(prob) > 9:
		key_num = f'{prob}'
	else:
		key_num = f'0{prob}'
	if int(hw) > 9:
		hw_num = f'{hw}'
	else:
		hw_num = f'0{hw}'
	key_folder = f'HW{key_num}Key'
	key_file = f'HW{hw_num}_Problem{key_num}_key.py'
	try:
		key_source_code = open(os.path.join(key_folder, key_file)).read()
	except FileNotFoundError:
		helper_tools.input.exit_msg(f'Please put {key_folder}/{key_file} inside {os.getcwd()}')
	key_output = helper_tools.files.PyRunner().RUN_FILE_WRAPPER(os.path.join(key_folder, key_file), temp_out)

	python_files = helper_tools.files.get_files(prob, 'py')
	run_files = []
	run_counter = 1
	for file in python_files:
		student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
		source_file = open(file, 'r').read()

		new_runner = helper_tools.files.PyRunner()
		print(f'\rRunning file {run_counter}        ', end='')
		run_counter += 1
		run_files.append({'name': student_name, 'source': source_file, 'out': new_runner.RUN_FILE_WRAPPER(file, temp_out)})
	print('')
	os.remove(temp_out)

	bad_reads = []
	for student in run_files:
		if student['out'] in helper_tools.files.MY_CLASS_ERROR_MESSAGES.values():
			bad_reads.append(student['name'])
	if len(bad_reads) == 0:
		print('There were no bad runs')
	else:
		print('Could not run:')
		for student in bad_reads:
			print(f'  {student}')

	io_data = helper_tools.io_data.IOResults({'source': key_source_code, 'out': key_output}, run_files)


def xlsx_grader(prob):
	print(f'Grading xlsx problem {prob}')


if __name__ == '__main__':
	helper_tools.input.validate_args(sys.argv)
	if sys.argv[2] == 'py':
		py_grader(sys.argv[3], sys.argv[1])
	if sys.argv[2] == 'xlsx':
		xlsx_grader(sys.argv[3])
