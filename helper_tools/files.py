import os
import re
import subprocess

import README

unicode_error_msg = 'UNICODE DECODE ERROR'
input_error_msg = 'FILE TERMINATED FOR USING INPUT'
general_error_msg = 'NO OUTPUT WAS GENERATED\n' \
                    'THIS MAY HAVE BEEN BECAUSE OF AN ERROR OR LOOP\n' \
                    'Check the console for error?'


def run_a_file(file_name, temp_out):

    if README.code_running_method == 1:
        # Plain os.system method - works except with infinite loops the file can get locked up
        os.system(rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1')

    if README.code_running_method == 2:
        # popen method - seems to be working the only sad thing is redirecting the error out
        file = open(temp_out, 'w')
        file.write(os.popen(rf'python "{os.path.join(os.getcwd(), file_name)}"').read())
        file.close()

    if README.code_running_method == 3:
        # subprocess method - file gets locked up after infinite loop
        command = rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1'
        subprocess.call(command, shell=True, close_fds=True)

    # Output file isn't getting freed up
    if README.code_running_method == 4:
        # experimental method
        os.popen(rf'python "{os.path.join(os.getcwd(), file_name)}" > {temp_out} 2>&1')


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
            source_code = open(file_name, 'r').read()
        except UnicodeDecodeError:
            source_code = unicode_error_msg
        if re.compile(r'input[ ]*\(').search(source_code) is not None:
            source_code = input_error_msg
        file_dict = {'name': student_name, 'net id': netid, 'source code': source_code, 'file name': file_name}
        if student_name in student_file_groups.keys():
            student_file_groups[student_name].append(file_dict)
        else:
            student_file_groups[student_name] = [file_dict]

    return student_file_groups

    # prob_re = re.compile(rf'problem.*{prob}')
    # part_re = re.compile(rf'part.*{prob}')
    # for file in all_files:
    #     if file.endswith(ftype) and (
    #             (prob_re.search(file.lower()) is not None) or (part_re.search(file.lower()) is not None)):
    #         good_files.append(file)
    # if len(good_files) == 0:
    #     helper_tools.input.exit_msg(f'No files for problem {prob} found')
    # return good_files
