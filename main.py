import os
import sys

import openpyexcel

import assets.py_file
import assets.xlsx_file
import helper_tools


def py_grader(prob, hw):
    print(f'Grading py problem {prob}')

    temp_out = 'TEMP_OUPUT_JOSH_GRADER.txt'
    if int(prob) > 9:
        key_num = f'{prob}'
    else:
        key_num = f'0{prob}'
    if int(hw) > 9:
        hw_num = f'{hw}'
    else:
        hw_num = f'0{hw}'
    key_folder = f'HW{key_num}Key'
    key_file = f'HW{hw_num}_Problem{key_num}_key.py'
    try:
        key_source_code = open(os.path.join(key_folder, key_file)).read()
    except FileNotFoundError:
        helper_tools.input.exit_msg(f'Please put {key_folder}/{key_file} inside {os.getcwd()}')
    key_output = helper_tools.files.PyRunner().RUN_FILE_WRAPPER(os.path.join(key_folder, key_file), temp_out)

    python_files = helper_tools.files.get_files(prob, 'py')
    run_files = []
    run_counter = 1
    for file in python_files:
        student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
        source_file = open(file, 'r').read()

        new_runner = helper_tools.files.PyRunner()
        print(f'{run_counter}) {file}')
        run_counter += 1
        run_files.append(
            {'name': student_name, 'source': source_file, 'out': new_runner.RUN_FILE_WRAPPER(file, temp_out), 'file name': file})
    print('')
    # os.remove(temp_out)

    bad_reads = []
    for student in run_files:
        if student['out'] in helper_tools.files.MY_CLASS_ERROR_MESSAGES.values():
            bad_reads.append(student['name'])
    if len(bad_reads) == 0:
        print('There were no bad runs')
    else:
        print('Could not run:')
        for student in bad_reads:
            print(f'  {student}')

    io_data = helper_tools.io_data.IOResults()
    io_data.populate({'source': key_source_code, 'out': key_output, 'file name': key_file}, run_files)
    assets.py_file.py_ui()


def xlsx_grader(hw):
    print('Grading xlsx')

    excel_files = []
    all_files = os.listdir('.')
    for file in all_files:
        if file.endswith('xlsx'):
            excel_files.append(file)

    if int(hw) > 9:
        hw_num = f'{hw}'
    else:
        hw_num = f'0{hw}'
    key_folder = f'HW{hw_num}Key'
    key_file = f'HW{hw_num}_key.xlsx'
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
            py_grader(sys.argv[3], sys.argv[1])
        except PermissionError:
            sys.stdout = out_ref
            helper_tools.input.exit_msg('Could not close temp out file - A file is timing out')

    if sys.argv[2] == 'xlsx':
        xlsx_grader(sys.argv[1])
