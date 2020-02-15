import datetime
import os

import helper_tools.config_reader as config


class Dirs:
    def __init__(self, hw_num):
        self.class_dir = config.hw_directory
        self.hw_dir = os.path.join(self.class_dir, f'HW {hw_num}')
        self.result_dir = os.path.join(self.hw_dir, config.report_folder_name + ' ' + str(datetime.datetime.now()))
        self.key_dir = os.path.join(self.hw_dir, f'HW{hw_num}Key')
