"""
Josh Bedwell's CH EN 263 Grader

This program runs and displays python or excel files in the when they are in the format that students submit
This program will take arguments in the following forms:
  {hw num} {py/xlsx}
If no arguments are given it will ask for parameters when the program starts.

Limitaions:
- There are diffrent methods for running the files. The biggest limitation is that if a student submits code with an
  infinite loop, the thread their code is on my stay alive even after the program terminates and ruin everything. The
  only way to stop it is killing the process or restarting the computer etc.
- The package being used for excel files only supports .xlsx files (not .xls etc.)
- There are some people putting fancy symbols in their code but the source code and outputs are stored in python strings
  which use utf-8 encoding so they will give a decode error.

Packages Required:
- PyQt5
- openpyexcel
"""

"""
Homeork location:
"""

hw_directory = r'C:\Users\josh-laptop\OneDrive\School\CH EN 263 TA'

r"""
Example file path this code is looking for:
  C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA\HW 2\Gradebook Bundled Download - Jan 22 2020\HW2Key
hw_directory variable given:
  r'C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA'
Where the student .py and .xlsx files are in the bundled download folder, and the answer key .py and .xlsx files are in
the HW2Key folder.

The homework folder must have the name "HW {hw num}".
Any download folder containing "Gradebook Bundled Download" will be accepted.
A key folder named "HW{any number of zeros}{hw num}Key" will be accepted.
All of the student and key files will have leading zeros stripped off of them.
"""

"""
Code running method:
"""

code_running_method = 0
pause_between_runs = False

"""
Method 0:
  Don't run code, just display source and no output. (Key code will always be run.)

Method 1 (CLEANEST):
  This method will plainly run a python command from your terminal and redirect it to the output file. This method is
  highly preferred except that its process may not die if the code it runs has an inifite loop.

Method 2 (SAFEST):
  This method is similar to the last except the function returns the output of the student's program to this program
  which then writes it to a file. This method is not affected by infinite loops in students' code, but it does not
  redirect their errors to the output file, they go to the console for this program.

Method 3:
  This method uses the more updated subprocess module instead of the os module, but it is also vulnerable to the
  unkilled process locking a file like method 1.
  
Method 4:
  This method attempts to run a command in the same way as method 2 which is not vulnerable to inifite loops, but rather
  than accept the output from the function return, redirect the student file output in the command. This method does not
  work because it says the file isn't found, but I really wish it did work.
"""

"""
Name of temporary file student output is written to:
"""

temprary_out_file_name = 'TEMP_OUPUT_JOSH_GRADER.txt'
temprary_error_out_name = 'TEMP_ERROR_OUTPUT.txt'

"""
Program time allowed:
"""

student_program_time_allowed = 5

"""
This is the amount of time in seconds a student's code is allowed to run before it is attempted to be terminated. 5
seconds should typically be long enough. If this number is left too high (>10), infintly printing student code will create a
large file that will be troublesome.
"""
