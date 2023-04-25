import json
import os
import re
import shutil
import sys

from pprint import pprint
from rich.console import Console
from rich.traceback import install
from rich.table import Table

install()
console = Console(record=True)

def get_expected_file_count_from_testname(test):
    num_str = test.split("S")[0].split('_')[-1]
    num_str = "".join(filter(str.isdigit, num_str))
    num = int(num_str)
    num += 1
    
    return num

assert(get_expected_file_count_from_testname('600s_100B_1P_13S_rel_mc_0dur_100lc') == 14)

def get_actual_file_count(testdir):
    test_files = os.listdir(testdir)
    csv_files_with_data = [os.path.join(testdir, file) for file in test_files if '.csv' in file and os.path.getsize( os.path.join(testdir, file) ) > 0]
    
    return len(csv_files_with_data)