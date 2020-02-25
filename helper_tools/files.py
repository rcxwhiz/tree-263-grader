import os
import threading
from os.path import join

import helper_tools.config_reader as config
import helper_tools.navigation
import helper_tools.student_results

error_msgs = {'unicode': '\n[GRADER] - Unicode decode error',
              'input': '\n[GRADER] - File terminated for using input',
              'long out': f'\n[GRADER] - File output was cut off because it is longer than {config.max_out_lines} '
                          f'lines\nThe full output is located in the output file for this script '
                          f'(if it is not set to be deleted)'}

results = helper_tools.student_results.PythonResults()


def read_file(file):
    return open(file, 'rt', encoding='utf-8').read()


def initialize_results():
    key_list = []
    stud_dict = {}
    navi = helper_tools.navigation.Dirs()

    # get key files
    for file in os.listdir(navi.key_dir):
        if file.endswith('.py'):
            source = read_file(join(navi.key_dir, file)).replace('\t', ' ' * 4)
            key_list.append({'source': source,
                             'file name': file,
                             'file path': join(navi.key_dir, file)})

    # get student files
    for stud_name in navi.students:
        stud_dict[stud_name] = []
        for file in os.listdir(join(navi.result_dir, stud_name)):
            if file.endswith('.py'):
                source = read_file(join(navi.result_dir, stud_name, file)).replace('\t', ' ' * 4)
                stud_dict[stud_name].append({'source': source,
                                             'file name': file,
                                             'file path': join(navi.result_dir, stud_name, file)})

    results.populate(key_list, stud_dict)


def run_files(dicts):
    # takes a list of dictionaries to run so that it can run the right number of threads easier
    base_threads = threading.active_count()
    if config.max_concurrent_programs == 0:
        max_threads = 1e9
    else:
        max_threads = base_threads + config.max_concurrent_programs
    num_run = 0
    threads = []
    while num_run < len(dicts):
        if threading.active_count() < max_threads:
            dict_obj = dicts[num_run]
            full_file_out = dict_obj['file path'][:-3] + '-' + config.file_out_name

            threads.append(threading.Thread(target=run_a_file,
                                            args=(join(dict_obj['file path']), full_file_out)))
            threads[-1].start()
            num_run += 1

    for thread in threads:
        thread.join()
    for dict_obj in dicts:
        full_file_out = dict_obj['file path'][:-3] + '-' + config.file_out_name

        output = read_file(full_file_out)
        output_by_lines = output.split('\n')
        if len(output_by_lines) > config.max_out_lines:
            output = '\n'.join(output_by_lines[:config.max_out_lines]) + error_msgs['long out']

        dict_obj['out'] = output
        if config.del_ouput_files:
            os.remove(full_file_out)


def run_key():
    run_files(results.key_files)


def run_student_files():
    all_files = []
    for student in results.student_files.keys():
        for file in results.student_files[student]:
            all_files.append(file)

    run_files(all_files)


def run_a_file(py_file, out_file):
    navi = helper_tools.navigation.Dirs()
    script_prefix = open(join(navi.scripts, 'exit-script-beginning.txt'), 'r').read().replace('TIME BEFORE KILL HERE', str(config.max_prog_time))
    student_script = read_file(py_file)
    script_postfix = open(join(navi.scripts, 'exit-script-end.txt'), 'r').read()
    temp_script_name = py_file[:-3] + '-MODIFIED.py'

    if 'input(' in student_script or 'input (' in student_script:
        open(out_file, 'w').write(error_msgs['input'])
        return

    open(temp_script_name, 'w', encoding='utf-8').write((script_prefix + student_script + script_postfix).replace('TIME BEFORE KILL HERE', str(config.max_prog_time)))
    os.system(f'python "{temp_script_name}" > "{out_file}" 2>&1')
    os.remove(temp_script_name)
