import os
import re
import sys
import threading
import math

import helper_tools

MY_CLASS_ERROR_MESSAGES = {'runtime issue': '[RUNTIME ISSUE]',
                           'timeout issue': '[TIMEOUT ISSUE]',
                           'input issue': '[USED INPUT]'}


def get_files(prob, ftype):
    all_files = os.listdir('.')
    good_files = []
    prob_re = re.compile(rf'problem.*{prob}')
    part_re = re.compile(rf'part.*{prob}')
    for file in all_files:
        if file.endswith(ftype) and (
                (prob_re.search(file.lower()) is not None) or (part_re.search(file.lower()) is not None)):
            good_files.append(file)
    if len(good_files) == 0:
        helper_tools.input.exit_msg(f'No files for problem {prob} found')
    return good_files


class PyRunner:

    def __init__(self):
        self.io_data = helper_tools.io_data.IOResults()

    def RUN_FILE_WRAPPER(self, _FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN):
        _MY_THREAD = ThreadWithTrace(target=self.RUN_A_FILE_IN,
                                     args=(_FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN))
        _MY_THREAD.start()
        _MY_THREAD.join(1)
        while _MY_THREAD.is_alive():
            _MY_THREAD.kill()
            open(_OUTPUT_FILE_NAME_AFTER_RUN, 'a').write(MY_CLASS_ERROR_MESSAGES['timeout issue'])
            print(MY_CLASS_ERROR_MESSAGES['timeout issue'], file=self.io_data.stdout_ref)
            _MY_THREAD.join()
        return open(_OUTPUT_FILE_NAME_AFTER_RUN, 'r').read()

    def RUN_A_FILE_IN(self, _FILE_IN_NAME_TO_RUN, _OUTPUT_FILE_NAME_AFTER_RUN):
        sys.stdout = open(_OUTPUT_FILE_NAME_AFTER_RUN, 'w')

        _FILE_ABOUT_TO_RUN = open(_FILE_IN_NAME_TO_RUN).read()
        if 'input' in _FILE_ABOUT_TO_RUN:
            open(_OUTPUT_FILE_NAME_AFTER_RUN, 'w').write(MY_CLASS_ERROR_MESSAGES['input issue'])
            print(MY_CLASS_ERROR_MESSAGES['input issue'], file=self.io_data.stdout_ref)
            sys.stdout = self.io_data.stdout_ref
            return None
        try:
            exec(_FILE_ABOUT_TO_RUN)
            sys.stdout = self.io_data.stdout_ref
        except Exception as BAD_NUTT:
            print('ERROR HERE ->', BAD_NUTT.args[0], file=self.io_data.stdout_ref)
            sys.stdout = self.io_data.stdout_ref
            open(_OUTPUT_FILE_NAME_AFTER_RUN, 'a').write(BAD_NUTT.args[0])
            print(MY_CLASS_ERROR_MESSAGES['runtime issue'], file=self.io_data.stdout_ref)


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
