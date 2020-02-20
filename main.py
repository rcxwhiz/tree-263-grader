import os
import shutil
import sys

import openpyexcel

import assets.py_ui
import assets.xlsx_ui
import helper_tools
import helper_tools.config_reader as config


def xlsx_grader(hw):
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

    excel_data = helper_tools.StudentResults.ExcelResults()
    excel_data.populate(key_sheets, student_sheets)
    assets.xlsx_ui.xlsx_ui()


if __name__ == '__main__':
    helper_tools.input.validate_args(sys.argv)
    if sys.argv[2] == 'py':

        helper_tools.input.initialize_files(sys.argv[1])
        navi = helper_tools.navigation.Dirs()

        helper_tools.files.initialize_results()

        print('Running key...')
        helper_tools.files.run_key()

        print('Running student files...')
        helper_tools.files.run_student_files()

        if config.cleanup_report:
            print('Deleting report directory...')
            shutil.rmtree(navi.result_dir)

        print('Launching UI.')
        assets.py_ui.py_ui()

    if sys.argv[2] == 'xlsx':

        print('Grading xlsx files...')
        xlsx_grader(sys.argv[1])
