from analyse_functions import *

if len(sys.argv) > 2:
    testdir = sys.argv[1]
    outputdir = sys.argv[2]
else:
    console.print(f"Using ./data for testdir and ./output for output.", style="bold white")
    testdir = "./data"
    outputdir = "./output"
