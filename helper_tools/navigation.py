import datetime
import os

import helper_tools.config_reader as config
import helper_tools.input


class Dirs:
    def __init__(self, hw_num):
        try:
            self.class_dir = config.hw_directory
            self.hw_dir = os.path.join(self.class_dir, f'HW {hw_num}')
            self.download_dir = ''
            for file in os.listdir(self.hw_dir):
                if 'Gradebook Bundled Download' in file and os.path.isdir(file):
                    self.download_dir = os.path.join(self.hw_dir, file)
                    break
            self.result_dir = os.path.join(self.hw_dir, config.report_folder_name + ' ' + str(datetime.datetime.now()))
            self.key_dir = os.path.join(self.hw_dir, f'HW{hw_num}Key')
        except FileNotFoundError:
            helper_tools.input.exit_msg(f'Trouble locating directory for hw {hw_num}\n'
                                        f'Please review directory structure in README.txt')
