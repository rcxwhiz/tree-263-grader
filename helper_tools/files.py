import datetime
import os
import threading
import sys

from os.path import join
import helper_tools.config_reader as config
import helper_tools.navigation
import helper_tools.StudentResults

unicode_error_msg = 'UNICODE DECODE ERROR'
input_error_msg = 'FILE TERMINATED FOR USING INPUT'
general_error_msg = 'NO OUTPUT WAS GENERATED\n' \
                    'THIS MAY HAVE BEEN BECAUSE OF AN ERROR OR LOOP\n' \
                    'Check the console for error?'

results = helper_tools.StudentResults.PythonResults()


def read_file(file):
    try:
        return open(file, 'r').read()
    except UnicodeDecodeError:
        return unicode_error_msg


def initialize_results():
    key_list = []
    stud_dict = {}
    navi = helper_tools.navigation.Dirs()

    # get key files
    for file in os.listdir(navi.key_dir):
        if file.endswith('.py'):
            try:
                source = open(file, 'r').read()
            except UnicodeDecodeError:
                source = unicode_error_msg
            key_list.append({'source': source, 'file name': file})

    # get student files
    for stud_name in navi.students:
        stud_dict[stud_name] = []
        for file in os.listdir(join(navi.result_dir, stud_name)):
            if file.endswith('.py'):
                try:
                    source = open(file, 'r').read()
                except UnicodeDecodeError:
                    source = unicode_error_msg
                stud_dict[stud_name].append({'source': source, 'file name': file})


def run_files(dicts):
    base_threads = threading.active_count()
    if config.max_concurrent_programs == 0:
        max_threads = 10000
    else:
        max_threads = base_threads + config.max_concurrent_programs
    num_run = 0
    threads = []
    while num_run < len(dicts):
        if threading.active_count() < max_threads:
            dict_obj = dicts[num_run]
            threads.append(threading.Thread(target=run_a_file,
                                            args=(join(dict_obj['file path'], dict_obj['file name']),
                                                  dict_obj['file name'] + config.file_out_name)))
            threads[-1].start()

    for thread in threads:
        thread.join()

    for dict_obj in dicts:
        dict_obj['out'] = read_file(join(dict_obj['file path'], config.file_out_name))
        if config.del_ouput_files:
            os.remove(join(dict_obj['file path'], config.file_out_name))


def run_key():
    run_files(results.key_files)


def run_a_file(py_file, out_file):
    script_prefix = open(join(sys.argv[0], 'scripts', 'exit-script-beginning.txt'), 'r').read()
    student_script = open(py_file, 'r').read()
    script_postfix = open(join(sys.argv[0], 'scripts', 'exit-script-end.txt'), 'r').read()
    temp_script_name = py_file[:-3] + '-MODIFIED.py'
    open(temp_script_name, 'w').write(script_prefix + student_script + script_postfix)
    os.system(rf'python "{temp_script_name}" > {out_file} 2>&1')
    os.remove(temp_script_name)


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
