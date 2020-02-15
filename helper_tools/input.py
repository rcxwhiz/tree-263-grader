import os
import re
import sys

import helper_tools.navigation


def exit_msg(msg):
    print('\n[ERROR]')
    print(msg)
    input('Press return to exit...')
    sys.exit()


def remove_zeros(name):
    name = re.sub(r'0+(\d)', r'\1', name)
    # name.replace('_', '')
    return name.lower()


def validate_args(args):

    if len(args) == 1:
        args.append(input('Enter the HW number: '))
        args.append(input('Enter the HW type (py/xlsx): '))
    elif len(args) == 2 or len(args) > 3:
        exit_msg(f'Valid arguments:\n'
                 f'[hw num] py [prob num]\n'
                 f'[hw num] xlsx')


def initialize_files(hw_num):
    dirs = helper_tools.navigation.Dirs()
    dirs.create_members(hw_num)
