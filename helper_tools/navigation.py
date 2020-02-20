from __future__ import annotations

import os
import shutil
from datetime import datetime
from os.path import join
from pathlib import Path
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
        self.project_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        self.scripts = join(str(self.project_dir.parent), 'scripts')

    def create_members(self, hw_num):
        print('Creating directories...')
        self.class_dir = config.hw_directory

        self.hw_dir = join(self.class_dir, f'HW {hw_num}')

        self.download_dir = ''
        try:
            for file in os.listdir(self.hw_dir):
                if 'Gradebook Bundled Download' in file:
                    self.download_dir = join(self.hw_dir, file)
                    break
        except FileNotFoundError:
            helper_tools.input.exit_msg(f'Could not find HW directory {self.hw_dir}\n'
                                        f'Directory structure given in README.md')

        self.key_dir = join(self.hw_dir, f'HW{hw_num}Key')

        try:
            for file in os.listdir(self.download_dir):
                if file.endswith('.py') or os.path.isdir(file):
                    os.rename(join(self.download_dir, file), join(self.download_dir, helper_tools.input.remove_zeros(file)))
        except FileNotFoundError:
            helper_tools.input.exit_msg(f'Issue with download directory {self.download_dir}\n'
                                        f'Directory structure given in README.md')
        try:
            for file in os.listdir(self.key_dir):
                os.rename(join(self.key_dir, file), join(self.key_dir, helper_tools.input.remove_zeros(file)))
        except FileNotFoundError:
            helper_tools.input.exit_msg(f'Issue with key directory {self.key_dir}\n'
                                        f'Directory structure given in README.md')
        dt = datetime.now()
        timestamp = f'[{dt.month}-{dt.day}-{str(dt.year)[:2]} {dt.hour};{dt.minute};{dt.second}]'
        self.result_dir = join(self.hw_dir, config.report_folder_name + ' ' + timestamp)
        os.mkdir(self.result_dir)

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

        self.check_for_empty_dirs()

    def check_for_empty_dirs(self):
        bad_studs = []
        for student in self.students:
            if len(os.listdir(join(self.result_dir, student))) == 0:
                shutil.rmtree(join(self.result_dir, student))
                # print(f'There were no files for {student}')
                bad_studs.append(student)
        for bad_stud in bad_studs:
            self.students.remove(bad_stud)
