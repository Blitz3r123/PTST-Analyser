# PTST Analyser

Analyses the test results to identify if the tests were successfull (contain all expected files) or not.

## Usage
```
python analyse.py <tests_directory> <output_directory> -copy
```

Where:

`tests_directory` is the directory containing all of the test folders where each test folder contains the pub and sub files.

`output_directory` is the destination directory for copying all the good tests to.