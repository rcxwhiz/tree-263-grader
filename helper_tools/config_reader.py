import configparser

reader = configparser.ConfigParser()

# TODO set working directory so that config file could be read

reader.read('config.ini')

run_code = reader.getboolean('Code Runtime', 'run_code')
max_concurrent_programs = reader.getint('Code Runtime', 'max_concurrent_programs')
max_prog_time = reader.getint('Code Runtime', 'max_prog_time')
del_ouput_files = reader.getboolean('Code Runtime', 'del_output_files')
cleanup_report = reader.getboolean('Code Runtime', 'cleanup_report')
max_out_lines = reader.getint('Code Runtime', 'max_out_lines')
ask_for_other_files = reader.getboolean('Code Runtime', 'ask_for_other_files')

hw_directory = reader.get('File Setup', 'hw_directory')
file_out_name = reader.get('File Setup', 'file_out_name')
report_folder_name = reader.get('File Setup', 'report_folder_name')
