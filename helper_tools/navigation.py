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
        self.data_dir = None
        self.project_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        self.scripts = join(str(self.project_dir.parent), 'scripts')

    def create_members(self, hw_num):
        if config.del_ouput_files:
            print('Script output files will be deleted after scripts run')
        else:
            print('Script output files will not be deleted after scripts run')
        if config.cleanup_report:
            print('Report directory will be deleted when program ends')
        else:
            print('Report directory will not be deleted when program ends')

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

        if os.path.exists(join(self.hw_dir, f'HW{hw_num}Data')):
            self.data_dir = join(self.hw_dir, f'HW{hw_num}Data')

        print('Moving student files...')
        self._populate_student_dirs()

    def _populate_student_dirs(self):
        extra_file_types = {}

        for student in self.students:
            # Put student .py files into folders
            for file in os.listdir(self.download_dir):
                if student in file and file.endswith('.py'):
                    shutil.copy(join(self.download_dir, file), join(self.result_dir, student, file))

        self.check_for_empty_dirs()

        # Give the student a copy of the data after we have checked if things are empty
        for student in self.students:
            student_types = set()
            for file in os.listdir(self.download_dir):
                # Grab the other file types
                if student in file:
                    ext = '.' + str(file.split('.')[-1])
                    if ext == file or ext == '.py':
                        continue
                    student_types.add(ext)

            # Add the extra file types from the student into the total
            for ext in student_types:
                if ext not in extra_file_types.keys():
                    extra_file_types[ext] = 1
                else:
                    extra_file_types[ext] += 1

            if self.data_dir is not None:
                for file in os.listdir(self.data_dir):
                    shutil.copy(join(self.data_dir, file), join(self.result_dir, student, file))

        # ask and put the extra files in
        if config.ask_for_other_files:
            self.print_extras(extra_file_types)
            for ext in extra_file_types.keys():
                response = input(f'Include {ext} in output directories? (y/n)\n')
                if response.lower() == 'y':
                    for file in os.listdir(self.download_dir):
                        for student in self.students:
                            if student in file and file.endswith(ext):
                                shutil.copy(join(self.download_dir, file), join(self.result_dir, student, file))
            print()

    def print_extras(self, dict_in):
        print('\nExtra types students submitted:')
        if not bool(dict_in):
            print('Only py types submitted')
        else:
            for ext in dict_in.keys():
                print(f'{ext} - {dict_in[ext]}/{len(self.students)} ({dict_in[ext] / len(self.students) * 100:.1f}%)')

    def check_for_empty_dirs(self):
        bad_studs = []
        for student in self.students:
            if len(os.listdir(join(self.result_dir, student))) == 0:
                shutil.rmtree(join(self.result_dir, student))
                # print(f'There were no files for {student}')
                bad_studs.append(student)
        for bad_stud in bad_studs:
            self.students.remove(bad_stud)
