import os
import re
import sys
import subprocess

import helper_tools


def run_a_file(file_name, temp_out):
    # Plain os.system method:
    # os.system(rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1')

    # popen method
    # file = open(temp_out, 'r')
    # file.write(os.popen(rf'python "{os.path.join(os.getcwd(), file_name)}"').read())
    # file.close()

    # subprocess method
    subprocess.call([rf'python "{os.path.join(os.getcwd(), file_name)}"',  '>',  rf'{temp_out} 2>&1'])



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
