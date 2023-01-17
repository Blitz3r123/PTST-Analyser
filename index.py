from functions import *

with open("data/progress.log", "r") as log_file:
    log = log_file.readlines()
    
tests = parse_tests(log)
            
for test in tests:
    test["duration_s"] = get_duration_s(test["duration"])
    
    if test["duration_s"] is not None:
        test["duration_m"] = test["duration_s"] / 60 
    else:
        test["duration_m"] = None
    
  
# ? Tests with a duration between 10 and 15 minutes  
good_tests = ([
    test
    for test in tests
    if 
        test["duration_m"] is not None
        and test["duration_m"] < 15
        and test["duration_m"] > 10
    
])

# ? Tests that took longer than expected with a duration => 15 minutes
long_tests = ([
    test
    for test in tests
    if 
        test["duration_m"] is not None
        and (
            test["duration_m"] == 15
            or test["duration_m"] > 15
        )
    
])

# ? Tests that took shorter than expected with a duration < 10 minutes
short_tests = ([
    test
    for test in tests
    if 
        test["duration_m"] is not None
        and test["duration_m"] < 10
    
])

output_test_type_stats(good_tests, short_tests, long_tests)

test_dirs = [
    os.path.join("data", dir)
    for dir in os.listdir("data") 
    if os.path.isdir( os.path.join("data", dir) )
]

# ---------------------------------------------------------------------------- #
#                              Good Tests Analysis                             #
# ---------------------------------------------------------------------------- #

good_test_dirs = list(
    set(
        [
            os.path.basename(test_dir) 
            for test_dir in test_dirs
        ]
    ) 
    & set(
        [
            test["test"] 
            for test in good_tests
        ]
    )
)


good_test_dirs = [
    os.path.join("data", good_test_dir)
    for good_test_dir in good_test_dirs
]

csv_file_mismatch_count = 0
for good_test_dir in good_test_dirs:
    
    run_dir_count = get_run_dir_count(good_test_dir)
    
    if run_dir_count == 0:
        console.print(
            os.path.basename(good_test_dir) + " has no run_n folders.", 
            style="bold red"
        )
        
    elif run_dir_count == 1:
        run_dir = [dir for dir in os.listdir(good_test_dir) if "run_" in dir][0]
        run_dir = os.path.join(good_test_dir, run_dir)
        
        csv_files = [file for file in os.listdir(run_dir) if '.csv' in file]
        
        if len(csv_files) == 0:
            console.print(
                os.path.basename(good_test_dir) + " has no .csv files in run_1.", 
                style="bold red"
            )
        else:
            # ? Check if the # of .csv files corresponds to the # of participants
            test_name = os.path.basename(good_test_dir)
            pub_count = get_pub_count(test_name)
            sub_count = get_sub_count(test_name)
            
            if (pub_count + sub_count) != len(csv_files):
                test_duration = [test["duration_m"] for test in tests if test["test"] == test_name][0]
                csv_file_mismatch_count += 1
                # console.print(f'\n{test_name}', style="bold red")
                # console.print(f'\tDuration (minutes): {"{:.0f}".format(test_duration)}', style="bold red")
                # console.print(
                #     f'\tMismatch between participant amount and number of .csv files produced for {test_name}.',
                #     style="bold red"
                # )
                # console.print(
                #     f'\tPubs (expected): {pub_count}\n\tSubs (expected): {sub_count}\n\tTotal (actual/expected): {len(csv_files)}/{pub_count + sub_count}',
                #     style="bold red"
                # )
            
            # ? Check if the .csv files produced had content
            for csv_file in csv_files:
                file_size_bytes = os.stat(os.path.join(run_dir, csv_file)).st_size
                if file_size_bytes == 0:
                    console.print(
                        os.path.join(run_dir, csv_file) + " is empty.", 
                        style="bold red"
                    )
        
    else:
        console.print(
            os.path.basename(good_test_dir) + " has multiple run_n folders.", 
            style="bold white"
        )

assert len( list(set([os.path.basename(test_dir) for test_dir in test_dirs]) & set([test["test"] for test in good_tests])) ) == len(good_tests)

# ---------------------------------------------------------------------------- #
#                              Long Tests Analysis                             #
# ---------------------------------------------------------------------------- #

long_test_dirs = list(
    set(
        [
            os.path.basename(test_dir) 
            for test_dir in test_dirs
        ]
    ) 
    & set(
        [
            test["test"] 
            for test in long_tests
        ]
    )
)

long_test_dirs = [
    os.path.join("data", long_test_dir)
    for long_test_dir in long_test_dirs
]

for long_test_dir in long_test_dirs:
    run_dir_count = get_run_dir_count(long_test_dir)
    
    if run_dir_count == 0:
        console.print(
            f'No run_n folders found for {os.path.basename(long_test_dir)}', 
            style="bold red"
        )
    elif run_dir_count > 1:
        console.print(
            f'Multiple run_n folders found for {os.path.basename(long_test_dir)}', 
            style="bold red"
        )
    else:
        run_dir = get_run_dir(long_test_dir)
        # ? Check for csv files
        csv_files = [x for x in os.listdir(run_dir) if '.csv' in x]
        
        if len(csv_files) > 0:
            console.print(
                f'csv files found for {os.path.basename(long_test_dir)}',
                style="bold green"
            )
            
long_test_names = [test["test"] for test in long_tests]

# ? Write short test names to a file to look for trends in the name
with open("long_tests.txt", "w") as f:
    f.writelines([" ".join(test["test"].split("_")) + "\n" for test in long_tests])

assert len( 
    list(
        set(
            [os.path.basename(test_dir) for test_dir in test_dirs]
        ) 
        & set(
            [test["test"] for test in long_tests]
        )
    ) 
) == len(long_tests)

# ---------------------------------------------------------------------------- #
#                             Short Tests Analysis                             #
# ---------------------------------------------------------------------------- #

short_test_dirs = list(
    set(
        [
            os.path.basename(test_dir) 
            for test_dir in test_dirs
        ]
    ) 
    & set(
        [
            test["test"] 
            for test in short_tests
        ]
    )
)

short_test_dirs = [
    os.path.join("data", short_test_dir)
    for short_test_dir in short_test_dirs
]

for short_test_dir in short_test_dirs:
    run_dir_count = get_run_dir_count(short_test_dir)
    
    if run_dir_count == 0:
        console.print(
            f'No run_n folders found for {os.path.basename(short_test_dir)}', 
            style="bold red"
        )
    elif run_dir_count > 1:
        console.print(
            f'Multiple run_n folders found for {os.path.basename(short_test_dir)}', 
            style="bold red"
        )
    else:
        run_dir = get_run_dir(short_test_dir)
        # ? Check for csv files
        csv_files = [x for x in os.listdir(run_dir) if '.csv' in x]
        
        if len(csv_files) > 0:
            console.print(
                f'csv files found for {os.path.basename(short_test_dir)}',
                style="bold green"
            )

# ? Write short test names to a file to look for trends in the name
with open("short_tests.txt", "w") as f:
    f.writelines([" ".join(test["test"].split("_")) + "\n" for test in short_tests])

assert len( 
    list(
        set(
            [os.path.basename(test_dir) for test_dir in test_dirs]
        ) 
        & set(
            [test["test"] for test in short_tests]
        )
    ) 
) == len(short_tests)