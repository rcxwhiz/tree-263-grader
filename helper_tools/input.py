import os
import re
import sys

import helper_tools
import helper_tools.config_reader as config


def exit_msg(msg):
    print('\n[ERROR]')
    print(msg)
    input('Press any key to exit...')
    sys.exit()


def remove_zeros(name):
    return re.sub(r'0+(\d)', r'\1', name)


def validate_args(args):

    if len(args) == 1:
        args.append(input('Enter the HW number: '))
        args.append(input('Enter the HW type (py/xlsx): '))
    elif len(args) == 2 or len(args) > 3:
        exit_msg(f'Valid arguments:\n'
                 f'[hw num] py [prob num]\n'
                 f'[hw num] xlsx')

    dirs = helper_tools.navigation.Dirs(args[1])

    try:
        os.chdir(os.path.join(config.hw_directory, 'HW ' + args[1]))
    except FileNotFoundError:
        exit_msg(f'Could not find the HW folder:\n'
                 f'{os.path.join(config.hw_directory, "HW " + args[1])}')
    hw_dirs = os.listdir('.')

    for cdir in hw_dirs:
        if 'Gradebook Bundled Download' in cdir:
            os.chdir(cdir)
            print(f'Finding hw files in:\n'
                  f'{os.getcwd()}')

            for file_name in os.listdir('.'):
                os.rename(file_name, remove_zeros(file_name))
            key_dir = os.path.join(f'HW{args[1]}Key')
            for file_name in os.listdir(key_dir):
                os.rename(os.path.join(key_dir, file_name), os.path.join(key_dir, remove_zeros(file_name)))

            return None
    exit_msg(f'Unable to find a Gradebook Bundled Download folder in:\n'
             f'{os.getcwd()}')
