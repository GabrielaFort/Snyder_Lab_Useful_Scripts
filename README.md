# Snyder_Lab_Useful_Scripts
Useful scripts for automating common tasks in the lab

### qPCR Analysis
```
usage: qpcr_analysis.py [-h] -f INPUT_FILE -s REF_SAMPLE [-c CYCLES] [-g REF_GENE] [-o OUTPUT_FILE]

This is a script for analyzing qPCR data using the ddcq analysis method.

options:
  -h, --help      show this help message and exit
  -f INPUT_FILE   Input csv file for qpcr analysis. Same format as automatically generated from Snyder lab thermocycler
  -s REF_SAMPLE   Supply name of reference sample.
  -c CYCLES       Optional: Input total number of cycles used for qPCR. Default = 40
  -g REF_GENE     Optional: Supply reference gene name. Default = Ppia
  -o OUTPUT_FILE  Optional: Supply name of output excel file. Default = qPCR_results
```

The `qpcr_analysis.py` script will analyze qPCR data using the delta delta Cq method. It takes a csv file as input containing columns corresponding to Sample, Target, and Cq. This sheet can be in the same format as is automatically exported from the thermocycler in the Snyder Lab. It returns an excel file containing new columns corresponding to the calculated delta Cq, delta delta Cq, and relative expression (relative to the input reference sample). 
