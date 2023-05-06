from analyse_functions import *

if len(sys.argv) >= 2:
    campdir = sys.argv[1]
elif len(sys.argv) == 1:
    console.print(f"No <campaign_directory> passed. Refer to README.md to find out about usage.", style="bold red")
    sys.exit()

if not os.path.exists(campdir):
    console.print(f"Path doesn't exist: {campdir}", style="bold red")
    sys.exit()

console.print(f"Reading files in {campdir}")
# ? Get the files in the campaign directory.
camp_files = [os.path.join(campdir, _) for _ in os.listdir(campdir)]

if len(camp_files) == 0:
    console.print(f"No files found in {campdir}. ", style="bold red")
    sys.exit()
    
progress_json_files = [file for file in camp_files if "progress.json" in file]
    
if len(progress_json_files) == 0:
    console.print(f"No progress.json files found in {campdir}.", style="bold red")
    sys.exit()
    
# ? Get the .txt files.
txt_files = [_ for _ in camp_files if '.txt' in _]

if len(txt_files) == 0:
    console.print(f"No output.txt files found in {campdir}.", style="bold red")
    sys.exit()
    
console.print(f"Reading tests from {campdir}...")
# ? Get the test folders from the campaign directory.
camp_dir_tests = [_ for _ in camp_files if os.path.isdir( _ )]

console.print("Reading progress.json...")
all_test_statuses = []

for progress_json_file in progress_json_files:
    # ? Get the test statuses from the progress.json.
    with open(progress_json_file) as f:
        progress_data = json.load(f)
        
    test_statuses = progress_data

    # ? Cross reference the available files with the test status tests.
    test_statuses = [item for item in test_statuses if item['test'] in [os.path.basename(_) for _ in camp_dir_tests] ]
    all_test_statuses.append(test_statuses)
    
all_test_statuses = sum(all_test_statuses, [])

console.print("Collecting test statuses...")
all_statuses = []
all_statuses_as_text = []

all_test_statuses = sorted(all_test_statuses, key=lambda x: x['start_time'])

for test in all_test_statuses:
    if "prolonged" in test['status'] or "fail" in test['status']:
        all_statuses.append("🔴")
        all_statuses_as_text.append(f"[bold red]{test['test']}[/bold red]")
    else:
        all_statuses.append("🟢")
        all_statuses_as_text.append(f"[bold green]{test['test']}[/bold green]")

all_statuses_output = ""
for i, item in enumerate(all_statuses):
    all_statuses_output += f"{item} "
    if (i + 1) % 20 == 0:
        all_statuses_output += "\n"
        
all_statuses_as_text = "\n".join(all_statuses_as_text)

try:
    assert( len(all_test_statuses) >= len(camp_dir_tests) )
except AssertionError as e:
    console.print(f"{e}", style="bold red")
    console.print(f"Tests not found in progress.json:", style="bold white")
    tests_with_no_status = [test for test in camp_dir_tests if os.path.basename(test) not in [item['test'] for item in all_test_statuses]]
    pprint(tests_with_no_status)
    console.print(f"\n", style="bold white")

    camp_dir_tests = [test for test in camp_dir_tests if test not in tests_with_no_status]
    
    assert( len(all_test_statuses) >= len(camp_dir_tests) )

console.print("Counting punctual and prolonged tests...")
total_tests_count = len(all_test_statuses)

punctual_tests = [test for test in all_test_statuses if test['status'] == 'punctual' or "success" in test['status']]
punctual_tests_count = len(punctual_tests)

prolonged_tests = [test for test in all_test_statuses if test['status'] == 'prolonged' or 'fail' in test['status']]
prolonged_tests_output = "\n".join(sorted([test['test'] for test in prolonged_tests]))
prolonged_tests_count = len(prolonged_tests)

console.print("Counting tests with expected files...")
# ? Find how many tests have expected number of files (that have data themselves).
tests_with_expected_files = []
for test in punctual_tests:
    testdir = os.path.join(campdir, test['test'])
    expected_file_count = get_expected_file_count_from_testname(test['test'])
    actual_file_count = get_actual_file_count(testdir)
    
    if expected_file_count == actual_file_count:
        tests_with_expected_files.append(test)
            
console.print("Building table...")   
table = Table(title=f"Analysis of {campdir}", show_lines=True, show_header=False)

table.add_row("Total Tests", f"{total_tests_count}")
table.add_row(f"[bold green]Punctual Tests[/bold green]", f"[bold green]{punctual_tests_count}[/bold green]")
table.add_row(f"[bold red]Prolonged Tests[/bold red]", f"[bold red]{prolonged_tests_count}[/bold red]")
table.add_row(f"[bold green]Usable Tests[/bold green]", f"[bold green]{len(tests_with_expected_files)}[/bold green]")
table.add_row("All Statuses (20 per row)", f"{all_statuses_output}")
table.add_row("[bold red]Prolonged Tests[/bold red]", f"[bold red]{prolonged_tests_output}[/bold red]")
table.add_row("All Tests", all_statuses_as_text)

console.print(table, style="bold white")

dest_path = os.path.dirname(campdir)

html_path = os.path.join( dest_path, f"{os.path.basename(campdir)}_analysis.html" )
console.save_html(html_path)

# ? Write punctual and prolonged tests to file.
with open( os.path.join( dest_path, f"{os.path.basename(campdir)}_punctual_tests.txt" ), "w" ) as f:
    for item in [test['test'] for test in punctual_tests]:
        f.write(f"{item}\n")

with open( os.path.join( dest_path, f"{os.path.basename(campdir)}_prolonged_tests.txt" ), "w" ) as f:
    for item in [test['test'] for test in prolonged_tests]:
        f.write(f"{item}\n")

if "-open" in sys.argv:
    if os.name == 'nt':
        os.startfile(dest_path)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        os.system('%s "%s"' % (opener, dest_path))