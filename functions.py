import os

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console(record=True)

from pprint import pprint

def parse_tests(log):
    tests = []
    
    for line in log:
        if "TEST: " in line:
            
            test_name = line.replace("TEST: ", "").strip()
            index = log.index(line)
            
            try:
                duration = log[index + 3]
                duration = duration.replace("[1/1]: ", "")
                duration = duration.strip()
                
                tests.append({
                    "test": test_name,
                    "duration": duration
                })
            
            except IndexError as e:
                # console.print(
                #     test_name + " has no duration.", 
                #     style="bold red"
                # )
                tests.append({
                    "test": test_name,
                    "duration": None
                })
    return tests

def get_duration_s(duration):
    if duration is None:
        return None
    else:
        time_periods = duration.split(":")
        
        duration_s = 0
        
        for time_period in time_periods:
            if "day" in time_period.lower():
                day_count = int(time_period.split(" Days")[0])
            elif "hour" in time_period.lower():
                hour_count = int(time_period.split(" Hours")[0])
            elif "minute" in time_period.lower():
                minute_count = int(time_period.split(" Minutes")[0])
            elif "second" in time_period.lower():
                second_count = int(time_period.split(" Seconds")[0])
                
        duration_s = duration_s + (
            day_count * 24 * 60 * 60
        )
        
        duration_s = duration_s + (
            hour_count * 60 * 60
        )
        
        duration_s = duration_s + (
            minute_count * 60
        )
        
        duration_s = duration_s + (
            second_count
        )
        
    return duration_s

assert get_duration_s("01 Days: 01 Hours: 01 Minutes: 01 Seconds") == 90061

def get_pub_count(test_name):
    return (int([x for x in test_name.split("_") if "P" in x][0].replace("P", "")))
    
def get_sub_count(test_name):
    return (int([x for x in test_name.split("_") if "S" in x][0].replace("S", "")))

def get_run_dir_count(test_dir):
    return len([ 
        child 
        for child in os.listdir( test_dir ) 
        if "run_" in child 
    ])
    
def get_run_dir(test_dir):
    return [os.path.join(test_dir, x) for x in os.listdir(test_dir) if 'run_' in x][0]

def get_avg_duration_m(tests):
    if len(tests) > 0:
        return sum([test["duration_m"] for test in tests]) / len(tests)
    else:
        return 0

def get_no_csv_files_count(tests):
    no_csv_file_count = 0
    for test in tests:
        dir = os.path.join("data", test["test"])
        run_dir = os.path.join(dir, "run_1")
        try:
            test_files = os.listdir(run_dir)
            if len([file for file in test_files if '.csv' in file]) == 0:
                no_csv_file_count += 1
        except FileNotFoundError as e:
            console.print(f'run_1 can\'t be found for {test}.', style="bold red")
            
    return no_csv_file_count

def get_is_missing_csv_files_count(tests):
    is_missing_csv_file_count = 0
    for test in tests:
        run_dir = os.path.join("data", test["test"], "run_1")
        try:
            test_files = os.listdir(run_dir)
            expected_pub_count = get_pub_count(test["test"])
            expected_sub_count = get_sub_count(test["test"])
            if len([file for file in test_files if '.csv' in file]) < expected_pub_count + expected_sub_count:
                is_missing_csv_file_count += 1
        except FileNotFoundError as e:
            console.print(f'run_1 can\'t be found for {test}.', style="bold red")
            
    return is_missing_csv_file_count

def get_avg_missing_csv_files_count(tests):
    total_file_count = 0
    for test in tests:
        run_dir = os.path.join("data", test["test"], "run_1")
        try:
            test_files = os.listdir(run_dir)
            expected_pub_count = get_pub_count(test["test"])
            expected_sub_count = get_sub_count(test["test"])
            csv_file_count = len([file for file in test_files if '.csv' in file])
            if csv_file_count < expected_pub_count + expected_sub_count:
                total_file_count += (expected_pub_count + expected_sub_count) - csv_file_count
        except FileNotFoundError as e:
            console.print(f'run_1 can\'t be found for {test}.', style="bold red")
            
    return "{:.0f}".format(total_file_count / len(tests)) if len(tests) > 0 else "0"

def output_test_type_stats(good, short, long):
    table = Table(title="Test Stats")
    
    table.add_column("Test \nStatus")
    table.add_column("Amount")
    table.add_column("Has \n.csv \nfiles", style="green")
    table.add_column("Are \nmissing \n.csv \nfiles", style="red")
    table.add_column("Avg. # of \n.csv files \nmissing", style="red")
    table.add_column("Avg. \nDuration \n(minutes)")
    
    data = [
        {
            "status": "Good", 
            "amount": f'{len(good)}', 
            "no_csv_files": str(get_no_csv_files_count(good)),
            "are_missing_csv_files": str(get_is_missing_csv_files_count(good)),
            "avg_missing_csv_files_count": str(get_avg_missing_csv_files_count(good)),
            "avg_duration_m": f'{"{:.0f}".format(get_avg_duration_m(good))}',
            "style": "bold green",
            "end_section": False
        },
        {
            "status": "Short", 
            "amount": f'{len(short)}', 
            "no_csv_files": str(get_no_csv_files_count(short)),
            "are_missing_csv_files": str(get_is_missing_csv_files_count(short)),
            "avg_missing_csv_files_count": str(get_avg_missing_csv_files_count(short)),
            "avg_duration_m": f'{"{:.0f}".format(get_avg_duration_m(short))}',
            "style": "bold dark_orange3",
            "end_section": False
        },
        {
            "status": "Long", 
            "amount": f'{len(long)}', 
            "no_csv_files": str(get_no_csv_files_count(long)),
            "are_missing_csv_files": str(get_is_missing_csv_files_count(long)),
            "avg_missing_csv_files_count": str(get_avg_missing_csv_files_count(long)),
            "avg_duration_m": f'{"{:.0f}".format(get_avg_duration_m(long))}',
            "style": "bold red",
            "end_section": True
        }
    ]
    
    for item in data:
        table.add_row(
            item["status"],
            item["amount"],
            item["no_csv_files"],
            item["are_missing_csv_files"],
            item["avg_missing_csv_files_count"],
            item["avg_duration_m"],
            end_section=item["end_section"],
            style=item["style"]
        )
    
    total_amount = f'{len(good) + len(short) + len(long)}'
    total_no_csv_files = get_no_csv_files_count(good)
    total_no_csv_files += get_no_csv_files_count(short)
    total_no_csv_files += get_no_csv_files_count(long)
    total_no_csv_files = "{:,.0f}".format(total_no_csv_files)
    
    total_is_missing_csv_files = get_is_missing_csv_files_count(good)
    total_is_missing_csv_files += get_is_missing_csv_files_count(short)
    total_is_missing_csv_files += get_is_missing_csv_files_count(long)
    total_is_missing_csv_files = "{:,.0f}".format(total_is_missing_csv_files)
    
    total_avg_missing_csv_files_count = get_avg_missing_csv_files_count(good + short + long)
    
    total_avg_duration_m = f'{"{:,.0f}".format(get_avg_duration_m(good + short + long))}'
    
    table.add_row(
        "All", 
        total_amount, 
        total_no_csv_files,
        total_is_missing_csv_files,
        total_avg_missing_csv_files_count,
        total_avg_duration_m,
        style="bold white"
    )

    console.print(table)
    console.save_html("output.html")