import os

from pprint import pprint

camp_dir = "C:/Users/acwh025/OneDrive - City, University of London/PhD/Experimental Tests/Data"

qos_camps = [os.path.join(camp_dir, x) for x in os.listdir(camp_dir) if "qos_combination_capture" in x and "fail" not in x]

tests = []

for camp in qos_camps:
    camp = os.path.join(camp, "the_only_set")
    camp_tests = [x for x in os.listdir(camp) if "progress.log" not in x]
    pprint(f"{os.path.basename(camp)}: {len(camp_tests)} tests")
    tests = tests + camp_tests
    
pprint(len(tests))