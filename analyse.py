from analyse_functions import *

if len(sys.argv) == 2:
    campdir = sys.argv[1]
elif len(sys.argv) == 1:
    console.print(f"No <campaign_directory> passed. Refer to README.md to find out about usage.", style="bold red")
    sys.exit()

if not os.path.exists(campdir):
    console.print(f"Path doesn't exist: {campdir}", style="bold red")
    sys.exit()

# ? Get the files in the campaign directory.
camp_files = [os.path.join(campdir, _) for _ in os.listdir(campdir)]

if len(camp_files) == 0:
    console.print(f"No files found in {campdir}. ", style="bold red")
    sys.exit()
    
if os.path.join(campdir, "progress.json") not in camp_files:
    console.print(f"No progress.json file found in {campdir}.", style="bold red")
    sys.exit()
    
# ? Get the .txt files.
txt_files = [_ for _ in camp_files if '.txt' in _]

if len(txt_files) == 0:
    console.print(f"No output.txt files found in {campdir}.", style="bold red")
    sys.exit()
    
# ? Get the test folders from the campaign directory.
camp_dir_tests = [_ for _ in camp_files if os.path.isdir( _ )]

# ? Get the test statuses from the progress.json.
with open(os.path.join(campdir, 'progress.json')) as f:
    progress_data = json.load(f)
    
test_statuses = progress_data

# ? Cross reference the available files with the test status tests.
test_statuses = [item for item in test_statuses if item['test'] in [os.path.basename(_) for _ in camp_dir_tests] ]

all_statuses = []
for status in [item['status'] for item in test_statuses]:
    if "prolonged" in status:
        all_statuses.append("🔴")
    else:
        all_statuses.append("🟢")

all_statuses_output = ""
for i, item in enumerate(all_statuses):
    all_statuses_output += f"{item} "
    if (i + 1) % 20 == 0:
        all_statuses_output += "\n"

assert( len(test_statuses) == len(camp_dir_tests) )

total_tests_count = len(test_statuses)

punctual_tests = [test for test in test_statuses if test['status'] == 'punctual']
punctual_tests_count = len(punctual_tests)

prolonged_tests = [test for test in test_statuses if test['status'] == 'prolonged']
prolonged_tests_output = "\n".join(sorted([test['test'] for test in prolonged_tests]))
prolonged_tests_count = len(prolonged_tests)

# ? Find how many tests have expected number of files (that have data themselves).
tests_with_expected_files = []
for test in punctual_tests:
    testdir = os.path.join(campdir, test['test'])
    expected_file_count = get_expected_file_count_from_testname(test['test'])
    actual_file_count = get_actual_file_count(testdir)
    
    if expected_file_count == actual_file_count:
        tests_with_expected_files.append(test)
        
table = Table(title=f"Analysis of {campdir}", show_lines=True, show_header=False)

table.add_row("Total Tests", f"{total_tests_count}")
table.add_row(f"[bold green]Punctual Tests[/bold green]", f"[bold green]{punctual_tests_count}[/bold green]")
table.add_row(f"[bold red]Prolonged Tests[/bold red]", f"[bold red]{prolonged_tests_count}[/bold red]")
table.add_row("All Statuses (20 per row)", f"{all_statuses_output}")
table.add_row("[bold red]Prolonged Tests[/bold red]", f"[bold red]{prolonged_tests_output}[/bold red]")

console.print(table, style="bold white")