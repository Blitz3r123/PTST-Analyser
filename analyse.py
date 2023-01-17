from analyse_functions import *

testdir = "./data"

# ? Path doesn't exist.
validate("if path exists", testdir)
    
# ? Path isn't a folder. 
validate("if path is a dir", testdir)

testdirs = get_testdirs(testdir)

# ? Path contains no folders.
validate("if path contains dirs", testdir)
    
progress_log = get_progress_log(testdir)

# ? No (or more than one) progress.log files found.
if not progress_log: 
    console.print(
        f'A single progress.log file has not been found in {testdir}.', 
        style="bold red"
    )
    sys.exit(0)

progress_log_tests = get_progress_log_tests(progress_log)

if not progress_log_tests:
    console.print(
        f'Error occured when reading {os.path.basename(progress_log)}.', 
        style="bold red"
    )
    sys.exit(0)
    
# ? Check number of test dirs matches the number of tests in progress.log
if len(progress_log_tests) != len(testdirs):
    console.print(f"Mismatch in number of tests found in the progress.log and the test folders found in {testdir}", style="bold red")
    console.print(f'\tprogress.log has {len(progress_log_tests)} tests while there are {len(testdirs)} test folders in {testdir}', style="bold white")
    sys.exit(0)
    
table = Table()
table.add_column("Test", no_wrap = False)
table.add_column("Expected Duration (s)", no_wrap = False)
table.add_column("Actual Duration (s)", no_wrap = False)
table.add_column("Expected .csv files", no_wrap = False)
table.add_column("Actual .csv files", no_wrap = False)
table.add_column("Log Files", no_wrap = False)

for test in testdirs:
    progress_test = [progress_test for progress_test in progress_log_tests if progress_test["test"] in test][0]
    
    expected_test_duration_s = get_expected_duration_s(test)
    actual_test_duration_s = parse_log_duration_to_s(progress_test["duration"])
    
    expected_csv_files = get_expected_csv_files(test)
    
    if expected_csv_files is None:
        expected_csv_files = ""
    else:
        expected_csv_files = "\n".join(expected_csv_files)
    
    actual_csv_files = get_actual_csv_files(test)
    
    if actual_csv_files is None:
        actual_csv_files = ""
    else:
        actual_csv_files = "\n".join(actual_csv_files)
    
    actual_logs = get_actual_logs(test)
    if actual_logs is None:
        actual_logs = ""
    else:
        actual_logs = "\n".join(actual_logs)
    
    table.add_row(
        test,
        str(expected_test_duration_s),
        str(actual_test_duration_s),
        expected_csv_files,
        actual_csv_files,
        actual_logs)
    
console.print(table)

with open("output.html", "w") as f:
    f.write(console.export_html())