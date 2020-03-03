import os

import openpyexcel

import assets
import helper_tools

unsupported_types = ['.ods', '.xls']


def xlsx_grader(hw):
    dirs = helper_tools.navigation.Dirs()
    dirs.create_members(hw)

    key_file_name = ''
    for file in os.listdir(dirs.key_dir):
        if file.endswith('.xlsx'):
            key_file_name = file
    if key_file_name == '':
        helper_tools.input.exit_msg(f'Could not find an excel file in {dirs.key_dir}')

    excel_files = []
    all_files = os.listdir(dirs.download_dir)

    for file in all_files:
        if file.endswith('.xlsx'):
            excel_files.append(file)
        else:
            for extenstion in unsupported_types:
                if file.endswith(extenstion):
                    print(f'{file} will not be opened')
                    break

    wb = openpyexcel.load_workbook(os.path.join(dirs.key_dir, key_file_name), data_only=True)

    key_sheets = {'file name': key_file_name, 'sheets': {}}
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

        wb = openpyexcel.load_workbook(os.path.join(dirs.download_dir, student_file), data_only=True)
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

    excel_data = helper_tools.student_results.ExcelResults()
    excel_data.populate(key_sheets, student_sheets)
    assets.xlsx_ui.xlsx_ui()
