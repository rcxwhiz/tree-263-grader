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
		_MY_THREAD = ThreadWithTrace(target=self.RUN_A_FILE_IN, args=(_FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN, _STRING_RESULT_TO_RETURN))
		_MY_THREAD.start()
		time.sleep(2)
		if _MY_THREAD.is_alive():
			print('Tried to kill a thread')
			_MY_THREAD.kill()
			_MY_THREAD.join()
			print(f'Thread alive: {_MY_THREAD.is_alive()}')
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


class ThreadWithTrace(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		threading.Thread.start(self)

	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, event, arg):
		if event == 'call':
			return self.localtrace
		else:
			return None

	def localtrace(self, frame, event, arg):
		if self.killed:
			if event == 'line':
				raise SystemExit()
		return self.localtrace

	def kill(self):
		self.killed = True
