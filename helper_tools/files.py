import os
import re

import helper_tools


def get_files(prob, ftype):
	all_files = os.listdir('.')
	good_files = []
	prob_re = re.compile(rf'problem.*{prob}')
	for file in all_files:
		if file.endswith(ftype) and prob_re.search(file.lower()) is not None:
			good_files.append(file)
	if len(good_files) == 0:
		helper_tools.input.exit_msg(f'No files for problem {prob} found')
	return good_files
