import configparser

reader = configparser.ConfigParser()
reader.read('config.ini')

run_code = reader.getboolean('Code Runtime', 'run_code')
max_concurrent_programs = reader.getint('Code Runtime', 'max_concurrent_programs')
max_prog_time = reader.getint('Code Runtime', 'max_prog_time')

hw_directory = reader.get('File Setup', 'hw_directory')
file_out_name = reader.get('File Setup', 'file_out_name')
