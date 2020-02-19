from __future__ import annotations

from datetime import datetime
import os
import shutil
from os.path import join
from typing import Optional
from pathlib import Path

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
        self.project_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        self.scripts = join(str(self.project_dir.parent), 'scripts')

    def create_members(self, hw_num):
        print('Creating directories...')
        try:
            self.class_dir = config.hw_directory

            self.hw_dir = join(self.class_dir, f'HW {hw_num}')

            self.download_dir = ''
            for file in os.listdir(self.hw_dir):
                if 'Gradebook Bundled Download' in file:
                    self.download_dir = join(self.hw_dir, file)
                    break

            self.key_dir = join(self.hw_dir, f'HW{hw_num}Key')

            for file in os.listdir(self.download_dir):
                os.rename(join(self.download_dir, file), join(self.download_dir, helper_tools.input.remove_zeros(file)))
            for file in os.listdir(self.key_dir):
                os.rename(join(self.key_dir, file), join(self.key_dir, helper_tools.input.remove_zeros(file)))

            dt = datetime.now()
            timestamp = f'[{dt.month}-{dt.day}-{str(dt.year)[:2]} {dt.hour};{dt.minute};{dt.second}]'
            self.result_dir = join(self.hw_dir, config.report_folder_name + ' ' + timestamp)
            os.mkdir(self.result_dir)

        except FileNotFoundError:
            helper_tools.input.exit_msg(f'Trouble locating directory for HW {hw_num}\n'
                                        f'Please review directory structure in README.txt')

        self.students = []
        for file in os.listdir(self.download_dir):
            if file.count('_') > 2:
                self.students.append('_'.join(file.split('_')[0:3]))

        self.students = list(set(self.students))

        for student in self.students:
            os.mkdir(join(self.result_dir, student))

        print('Moving student files...')
        self._populate_student_dirs()

    def _populate_student_dirs(self):
        for student in self.students:
            for file in os.listdir(self.download_dir):
                if student in file and file.endswith('.py'):
                    shutil.copy(join(self.download_dir, file), join(self.result_dir, student, file))
            if len(os.listdir(join(self.result_dir, student))) == 0:
                os.removedirs(join(self.result_dir, student))
                self.students.remove(student)
