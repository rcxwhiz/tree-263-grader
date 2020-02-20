# TODO think about a solution to files that generate and show plots
# TODO Improve message for unopened excel files
# TODO find a way to save or display plots that are made on the fly, maybe a saveall plt command?

Josh Bedwell's CH EN 263 Grader

This program runs and displays python or excel files in the when they are in the format that students submit
This program will take arguments in the following forms:
  {hw num} {py/xlsx}
If no arguments are given it will ask for parameters when the program starts.

Limitaions:
- The package being used for excel files only supports .xlsx files (not .xls etc.)
- If the students are doing a lot of graphical things that doesn't go so well.

Packages Required:
- PyQt5
- openpyexcel

Homeork location:

hw_directory = r'C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA'

Example file path this code is looking for:
  C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA\HW 2\Gradebook Bundled Download - Jan 22 2020\
  C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA\HW 2\HW2Key
hw_directory variable given:
  r'C:\Users\josh-desktop\OneDrive\School\CH EN 263 TA'
Where the student .py and .xlsx files are in the bundled download folder, and the answer key .py and .xlsx files are in
the HW2Key folder.

The homework folder must have the name "HW {hw num}".
Any download folder containing "Gradebook Bundled Download" will be accepted.
A key folder named "HW{any number of zeros}{hw num}Key" will be accepted.
All of the student and key files will have leading zeros stripped off of them.
