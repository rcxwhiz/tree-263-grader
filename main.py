import multiprocessing
import os
import sys

import openpyexcel

import assets.py_file
import assets.xlsx_file
import helper_tools


# def py_grader(prob, hw):
#     print(f'Grading py problem {prob}\n')
#     io_data = helper_tools.io_data.IOResults()
#     io_data.set_stdout_ref(sys.stdout)
#
#     temp_out = 'TEMP_OUPUT_JOSH_GRADER.txt'
#     key_folder = f'HW{hw}Key'
#     key_file = f'HW{hw}_Problem{prob}_key.py'
#     try:
#         key_source_code = open(os.path.join(key_folder, key_file)).read()
#     except FileNotFoundError:
#         helper_tools.input.exit_msg(f'Please put {key_folder}/{key_file} inside {os.getcwd()}')
#
#     if 'input' in key_source_code:
#         key_output = 'Terminated for using input'
#     else:
#         key_output = helper_tools.files.run_a_file(os.path.join(key_folder, key_file), temp_out)
#
#     student_python_files = helper_tools.files.get_files(prob, 'py')
#     run_files = []
#     run_counter = 1
#     for file in student_python_files:
#         student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
#         try:
#             source_file = open(file, 'r').read()
#         except UnicodeDecodeError:
#             run_files.append({'name': student_name,
#                               'source': '[UNICODE DECODE ERROR]',
#                               'out': '[UNICODE DECODE ERROR]',
#                               'file name': file})
#             continue
#
#         print(f'{run_counter}) {file}')
#         run_counter += 1
#
#         if 'input' in source_file:
#             open(temp_out, 'w').write('Terminated for using input')
#         else:
#             student_run_p = multiprocessing.Process(target=helper_tools.files.run_a_file, args=(file, temp_out))
#             student_run_p.start()
#             student_run_p.join(helper_tools.input.program_time_allowed)
#             while student_run_p.is_alive():
#                 print(f'Terminating {file}')
#                 student_run_p.terminate()
#                 student_run_p.join()
#
#         run_files.append({'name': student_name,
#                           'source': source_file,
#                           'out': open(temp_out, 'r').read(),
#                           'file name': file})
#         os.remove(temp_out)
#     print('Complete')
#
#     io_data.populate({'source': key_source_code, 'out': key_output, 'file name': key_file}, run_files)
#     assets.py_file.py_ui()


def xlsx_grader(hw):
    print('Grading xlsx')

    excel_files = []
    all_files = os.listdir('.')
    for file in all_files:
        if file.endswith('xlsx'):
            excel_files.append(file)

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
            # py_grader(sys.argv[3], sys.argv[1])

            prob = sys.argv[3]
            hw = sys.argv[1]
            print(f'Grading py problem {prob}\n')
            io_data = helper_tools.io_data.IOResults()
            io_data.set_stdout_ref(sys.stdout)

            temp_out = 'TEMP_OUPUT_JOSH_GRADER.txt'
            key_folder = f'HW{hw}Key'
            key_file = f'HW{hw}_Problem{prob}_key.py'
            try:
                key_source_code = open(os.path.join(key_folder, key_file)).read()
            except FileNotFoundError:
                helper_tools.input.exit_msg(f'Please put {key_folder}/{key_file} inside {os.getcwd()}')

            if 'input' in key_source_code:
                key_output = 'Terminated for using input'
            else:
                helper_tools.files.run_a_file(os.path.join(key_folder, key_file), temp_out)
                key_output = open(temp_out, 'r').read()

            student_python_files = helper_tools.files.get_files(prob, 'py')
            run_files = []
            run_counter = 1
            for file in student_python_files:
                student_name = f'{file.split("_")[1]} {file.split("_")[0]}'
                try:
                    source_file = open(file, 'r').read()
                except UnicodeDecodeError:
                    run_files.append({'name': student_name,
                                      'source': '[UNICODE DECODE ERROR]',
                                      'out': '[UNICODE DECODE ERROR]',
                                      'file name': file})
                    continue

                print(f'{run_counter}) {file}')
                run_counter += 1

                if 'input' in source_file:
                    open(temp_out, 'w').write('Terminated for using input')
                else:
                    student_run_p = multiprocessing.Process(target=helper_tools.files.run_a_file, args=(file, temp_out))
                    student_run_p.start()
                    student_run_p.join(helper_tools.input.program_time_allowed)
                    student_run_p.terminate()
                    student_run_p.join()

                run_files.append({'name': student_name,
                                  'source': source_file.replace('\t', ' ' * 4),
                                  'out': open(temp_out, 'r').read(),
                                  'file name': file})
                # os.remove(temp_out)
            print('Complete')

            io_data.populate({'source': key_source_code, 'out': key_output, 'file name': key_file}, run_files)
            assets.py_file.py_ui()
        except PermissionError:
            sys.stdout = out_ref
            helper_tools.input.exit_msg('Could not close temp out file - A file is timing out')

    if sys.argv[2] == 'xlsx':
        xlsx_grader(sys.argv[1])
