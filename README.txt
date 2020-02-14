Josh Bedwell's CH EN 263 Grader

This program runs and displays python or excel files in the when they are in the format that students submit
This program will take the following arguments:
  {hw num} {py/xlsx}
If no arguments are given it will ask for parameters when the program starts.

Limitaions:
- The package being used for excel files only supports .xlsx files (not .xls etc.)
- There are some people putting fancy symbols in their code but the source code and outputs are stored in python strings
  which use utf-8 encoding so they will give a decode error.
- You cannot see graphs made in excel and you cannot see unsaved graphs from python

Packages Required:
- PyQt5
- openpyexcel
- configparser