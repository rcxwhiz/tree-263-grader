from __future__ import annotations

import datetime
import os
import shutil
from os.path import join
from typing import Optional

import helper_tools.config_reader as config
import helper_tools.input


class DirsMeta(type):
    _instance: Optional[Dirs] = None

    def __call__(self) -> Dirs:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Dirs(metaclass=DirsMeta):
    def __init__(self):
        self.class_dir = None
        self.hw_dir = None
        self.download_dir = None
        self.result_dir = None
        self.key_dir = None
        self.students = None

    def create_members(self, hw_num):
        print('Creating directories...')
        try:
            self.class_dir = config.hw_directory

            self.hw_dir = join(self.class_dir, f'HW {hw_num}')

            self.download_dir = ''
            for file in os.listdir(self.hw_dir):
                if os.path.isdir(file) and 'Gradebook Bundled Download' in file:
                    self.download_dir = join(self.hw_dir, file)
                    break

            self.result_dir = join(self.hw_dir, config.report_folder_name + ' ' + str(datetime.datetime.now()))
            os.mkdir(self.result_dir)

            self.key_dir = join(self.hw_dir, f'HW{hw_num}Key')

        except FileNotFoundError:
            helper_tools.input.exit_msg(f'Trouble locating directory for hw {hw_num}\n'
                                        f'Please review directory structure in README.txt')

        self.students = []
        for file in os.listdir('.'):
            if file.count('_') > 2:
                self.students.append(''.join(file.split('_')[0:3]))

        for student in self.students:
            os.mkdir(join(self.result_dir, student))

        print('Moving student files...')
        self._populate_student_dirs()

    def _populate_student_dirs(self):
        for student in self.students:
            for file in os.listdir(self.download_dir):
                if student in file and file.endswith('.py'):
                    shutil.copy(join(self.download_dir, file), join(self.result_dir, student, file))
