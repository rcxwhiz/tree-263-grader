import os
import re
import sys
import threading
import time

import helper_tools
MY_CLASS_ERROR_MESSAGES = {'runtime issue': 'COULD NOT RUN',
                   'timeout issue': 'TIMED OUT'}


def get_files(prob, ftype):
	all_files = os.listdir('.')
	good_files = []
	prob_re = re.compile(rf'problem.*{prob}')
	part_re = re.compile(rf'part.*{prob}')
	for file in all_files:
		if file.endswith(ftype) and ((prob_re.search(file.lower()) is not None) or (part_re.search(file.lower()) is not None)):
			good_files.append(file)
	if len(good_files) == 0:
		helper_tools.input.exit_msg(f'No files for problem {prob} found')
	return good_files


class PyRunner:

	def RUN_FILE_WRAPPER(self, _FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN):
		_STRING_RESULT_TO_RETURN = ''
		_MY_THREAD = threading.Thread(target=self.RUN_A_FILE_IN, args=(_FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN, _STRING_RESULT_TO_RETURN))
		_MY_THREAD.start()
		_MY_THREAD.join(2)
		if _MY_THREAD.is_alive():
			# TODO how to kill a thread?????
			_MY_THREAD.
			_STRING_RESULT_TO_RETURN = MY_CLASS_ERROR_MESSAGES['timeout issue']
		return _STRING_RESULT_TO_RETURN

	def RUN_A_FILE_IN(self, _FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN, _STRING_RESULT_TO_RETURN):
		_TEMPORARY_STDOUT_MARKER = sys.stdout
		sys.stdout = open(_OUTPUT_FILE_NAME_AFTER_RUN, 'w')
		try:
			exec(open(_FILE_IN_NAME_TO_RUN).read())
			sys.stdout = _TEMPORARY_STDOUT_MARKER
			return open(_OUTPUT_FILE_NAME_AFTER_RUN, 'r').read()
		except Exception:
			print(f'Could not read {_FILE_IN_NAME_TO_RUN}')
			sys.stdout = _TEMPORARY_STDOUT_MARKER
			return MY_CLASS_ERROR_MESSAGES['runtime issue']
