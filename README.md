# PTST Analyser

Analyses the test campaign data. 

You pass in the folder directory and it will list the following:
- how many tests were punctual/prolonged
- how many punctual tests had all of the expected data
    - i.e. contains the expected number of files and all files are not empty
- a list of the prolonged tests
    - possible trends in the prolonged test settings

## Usage
```
python <campaign_directory>
```

`<campaign_directory>`: Directory pointing to the test campaign data.

The `<campain_directory>` should contain the following file structure:
```
- <campaign_name>
    - 600s_100B_50P_50S_rel_mc_3dur_100lc
    - ...
    - 600s_100B_50P_50S_rel_uc_3dur_100lc
    - progress.json
    - <campaign_name>_output.txt
```

**Make sure the `progress.json` and `<campaign_name>_output.txt` files are present.**