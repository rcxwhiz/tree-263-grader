import os
import re
import sys

import helper_tools.navigation


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

    # TODO this should probably happen in the Dirs class and not here
    for file in os.listdir(dirs.download_dir):
        os.rename(os.path.join(dirs.download_dir, file), os.path.join(dirs.download_dir, remove_zeros(file)))
    for file in os.listdir(dirs.key_dir):
        os.rename(os.path.join(dirs.key_dir, file), os.path.join(dirs.key_dir, remove_zeros(file)))
