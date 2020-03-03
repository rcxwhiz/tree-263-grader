import shutil
import sys

import assets.xlsx_ui
import helper_tools
import helper_tools.config_reader as config

if __name__ == '__main__':
    helper_tools.input.validate_args(sys.argv)
    if sys.argv[2] == 'py':
        print(f'\nGrading HW {sys.argv[1]} python problems...')

        helper_tools.input.initialize_files(sys.argv[1])
        navi = helper_tools.navigation.Dirs()

        helper_tools.files.initialize_results()

        print('Running key...')
        helper_tools.files.run_key()

        print('Running student files...')
        helper_tools.files.run_student_files()

        print('Launching UI...')
        assets.py_ui.py_ui()

        if config.cleanup_report:
            print('Deleting report directory...')
            shutil.rmtree(navi.result_dir)

    if sys.argv[2] == 'xlsx':

        print('Grading xlsx files...')
        helper_tools.excel_grading.xlsx_grader(sys.argv[1])
