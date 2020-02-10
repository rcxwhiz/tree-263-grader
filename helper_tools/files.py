import os
import re
import subprocess
import sys

import README
import helper_tools


def run_a_file(file_name, temp_out):

    if README.code_running_method == 1:
        # Plain os.system method - works except with infinite loops the file can get locked up
        os.system(rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1')

    if README.code_running_method == 2:
        # popen method - seems to be working the only sad thing is redirecting the error out
        temp_err_ref = sys.stderr
        sys.stderr = open(README.temprary_error_out_name, 'r')
        file = open(temp_out, 'w')
        file.write(os.popen(rf'python "{os.path.join(os.getcwd(), file_name)}"').read())
        file.close()
        sys.stderr.close()
        sys.stderr = temp_err_ref

    if README.code_running_method == 3:
        # subprocess method - file gets locked up after infinite loop
        command = rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1'
        subprocess.call(command, shell=True, close_fds=True)

    # Output file isn't found???
    if README.code_running_method == 4:
        os.popen(rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1')


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
