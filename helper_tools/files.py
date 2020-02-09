import os
import re
import sys

import helper_tools


def run_a_file(file_name, temp_out):
    os.system(rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1')
    result = open(temp_out, 'r').read()
    return result


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
