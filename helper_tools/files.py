import datetime
import os
import threading
import subprocess

from os.path import join
import helper_tools.config_reader as config
import helper_tools.navigation

unicode_error_msg = 'UNICODE DECODE ERROR'
input_error_msg = 'FILE TERMINATED FOR USING INPUT'
general_error_msg = 'NO OUTPUT WAS GENERATED\n' \
                    'THIS MAY HAVE BEEN BECAUSE OF AN ERROR OR LOOP\n' \
                    'Check the console for error?'

navi = helper_tools.navigation.Dirs('')


def read_file(file):
    try:
        return open(file).read()
    except UnicodeDecodeError:
        return unicode_error_msg


def run_files(dicts):
    base_threads = threading.active_count()
    if config.max_concurrent_programs == 0:
        for dict in dicts:
            run_a_file(dict['source code'])
    else:
        # TODO finish this part where it spawns the right number of threads
        while threading.active_count() < base_threads + config.max_concurrent_programs:


def run_key():
    base_threads = threading.active_count()
    for file in os.listdir(navi.key_dir):
        if file.endswith('.py'):
            file_name = file
            source_code = read_file(join(navi.key_dir, file))
            # TODO this part is just going to make a list of dicts, give that to run_files, and run_files will take care of assembling dict stuff
            out = run_a_file(file, config.file_out_name)
            out = read_file(config.file_out_name)


def run_a_file(py_file, out_file):
    # TODO append the kill sript at the top of the file
    os.system(rf'python "{py_file}" > {out_file} 2>&1')


def get_py_files():
    all_files = os.listdir('.')
    all_py_files = []
    for file in all_files:
        if file.endswith('.py'):
            all_py_files.append(file)

    student_file_groups = {}

    for file_name in all_py_files:
        student_name = file_name.split('_')[1] + ' ' + file_name.split('_')[0]
        netid = file_name.split('_')[2]
        try:
            source_code = open(file_name, 'r').read().replace('\t', ' ' * 4)
        except UnicodeDecodeError:
            source_code = unicode_error_msg
        file_dict = {'name': student_name, 'net id': netid, 'source code': source_code, 'file name': file_name}
        if student_name in student_file_groups.keys():
            student_file_groups[student_name].append(file_dict)
        else:
            student_file_groups[student_name] = [file_dict]

    return student_file_groups
