import os
import sys

supported_files = ['py', 'xlsx']
hw_directory = r'C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA'


def exit_msg(msg):
    print('[ERROR]')
    print(msg)
    input('Press any key to exit...')
    sys.exit()


def validate_args(args):
    if len(args) == 4:
        if args[2] != 'py':
            exit_msg(f'Valid arguments:\n'
                     f'[hw num] py [prob num]\n'
                     f'[hw num] xlsx')
    elif len(args) == 3:
        if args[2] != 'xlsx':
            exit_msg(f'Valid arguments:\n'
                     f'[hw num] py [prob num]\n'
                     f'[hw num] xlsx')
    elif len(args) == 1:
        args.append(input('Enter the HW number: '))
        args.append(input('Enter the HW type (py/xlsx): '))
        if args[2] == 'py':
            args.append(input('Enter the problem number: '))
    try:
        os.chdir(os.path.join(hw_directory, 'HW ' + args[1]))
    except FileNotFoundError:
        exit_msg(f'Could not find the HW folder:\n'
                 f'{os.path.join(hw_directory, "HW " + args[1])}')
    hw_dirs = os.listdir('.')
    for cdir in hw_dirs:
        if 'Gradebook Bundled Download' in cdir:
            os.chdir(cdir)
            print(f'Finding hw files in:\n'
                  f'{os.getcwd()}')
            return None
    exit_msg(f'Unable to find a Gradebook Bundled Download folder in:\n'
             f'{os.getcwd()}')
