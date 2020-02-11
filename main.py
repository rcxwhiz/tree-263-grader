import multiprocessing
import os
import re
import sys

import openpyexcel

import README
import assets.py_file
import assets.xlsx_file
import helper_tools


def xlsx_grader(hw):
    print('Grading xlsx problems\n')

    excel_files = []
    all_files = os.listdir('.')
    for file in all_files:
        if file.endswith('.xlsx'):
            excel_files.append(file)
        elif not file.endswith('.py'):
            print(f'{file} will not be opened')

    key_folder = f'HW{hw}Key'
    key_file = f'HW{hw}_key.xlsx'
    key_sheets = {'file name': key_file, 'sheets': {}}

    try:
        wb = openpyexcel.load_workbook(os.path.join(key_folder, key_file), data_only=True)
    except FileNotFoundError:
        helper_tools.input.exit_msg(f'Please put {key_folder}/{key_file} inside {os.getcwd()}')

    for sheet_name in wb.sheetnames:
        arr = []
        sheet = wb[sheet_name]
        for row in sheet.iter_rows():
            arr.append([])
            for cell in row:
                arr[-1].append(cell.value)
        key_sheets['sheets'][sheet_name] = arr

    student_sheets = []
    for student_file in excel_files:

        wb = openpyexcel.load_workbook(student_file, data_only=True)
        student_sheet_builder = {}
        for sheet_name in wb.sheetnames:
            arr = []
            sheet = wb[sheet_name]
            for row in sheet.iter_rows():
                arr.append([])
                for cell in row:
                    arr[-1].append(cell.value)
            student_sheet_builder[sheet_name] = arr

        student_name = f'{student_file.split("_")[1]} {student_file.split("_")[0]}'
        student_sheets.append({'name': student_name, 'file name': student_file, 'sheets': student_sheet_builder})

    excel_data = helper_tools.io_data.ExcelResults()
    excel_data.populate(key_sheets, student_sheets)
    assets.xlsx_file.xlsx_ui()


if __name__ == '__main__':
    helper_tools.input.validate_args(sys.argv)
    out_ref = sys.stdout
    if sys.argv[2] == 'py':
        try:
            hw = sys.argv[1]
            print(f'Grading py problems\n')
            io_data = helper_tools.io_data.IOResults()
            io_data.set_stdout_ref(sys.stdout)

            key_folder = f'HW{hw}Key'
            key_files = []
            for key in os.listdir(key_folder):
                if key.endswith('.py'):
                    key_files.append({'file name': key})

            input_re = re.compile(r'input[ ]*\(')

            for key_file in key_files:
                try:
                    key_file['source code'] = open(os.path.join(key_folder, key_file['file name'])).read()
                except UnicodeDecodeError:
                    key_file['source code'] = helper_tools.files.unicode_error_msg
                    key_file['out'] = helper_tools.files.unicode_error_msg
                    continue
                if input_re.search(key_file['source code']) is not None:
                    key_file['source code'] = helper_tools.files.input_error_msg
                    key_file['out'] = helper_tools.files.input_error_msg
                    continue
                key_run_p = multiprocessing.Process(target=helper_tools.files.run_a_file,
                                                    args=(os.path.join(key_folder, key_file['file name']),
                                                          README.temprary_out_file_name))
                key_run_p.start()
                key_run_p.join(README.student_program_time_allowed)
                key_run_p.terminate()
                key_run_p.join()

                key_file['out'] = open(README.temprary_out_file_name).read()

            num_files_run = 1
            student_python_file_groups = helper_tools.files.get_py_files()
            for student in student_python_file_groups:
                for student_file in student_python_file_groups[student]:
                    print(f'{num_files_run}) {student_file["file name"]} ->', end=' ')
                    if student_file['source code'] == helper_tools.files.unicode_error_msg:
                        student_file['out'] = helper_tools.files.unicode_error_msg
                    elif re.compile(r'input[ ]*\(').search(student_file['source code']) is not None:
                        student_file['out'] = helper_tools.files.input_error_msg
                    else:
                        student_run_p = multiprocessing.Process(target=helper_tools.files.run_a_file,
                                                                args=(student_file['file name'],
                                                                      README.temprary_out_file_name))
                        student_run_p.start()
                        student_run_p.join(README.student_program_time_allowed)
                        student_run_p.terminate()
                        student_run_p.join()
                        student_file['out'] = open(README.temprary_out_file_name, 'r').read()
                        if student_file['out'] == '':
                            student_file['out'] = helper_tools.files.general_error_msg
                    print('finished')
                    num_files_run += 1
                    if README.pause_between_runs:
                        input()

            print('Complete')

            io_data.populate(key_files, student_python_file_groups)
            assets.py_file.py_ui()
            os.remove(README.temprary_out_file_name)
        except PermissionError:
            sys.stdout = out_ref
            helper_tools.input.exit_msg('Could not close temp out file - A file is timing out')

    if sys.argv[2] == 'xlsx':
        xlsx_grader(sys.argv[1])
