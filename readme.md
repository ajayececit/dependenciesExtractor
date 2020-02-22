# Dependencies Extractor

This helps to extract all the import statements from a python file by iterating through folders and subfolders

## Getting Started

Clone the repo to the local machine and run the dependencies script.

### Run the script from terminal

* To iterate through single python file py dependencies.py --file {filepath}
* To iterate through all the python files in folders and subfolder py dependencies.py --folder {folderpath}

### Output
Once the script ran successfully following files will get generated in {givenpath}/output

* dependencies_list - which will have all the import statements from all the python files
* import_maper - which will have the line number and file name of all the import statements
* used_dependencies - which will have only the modules used in the python files