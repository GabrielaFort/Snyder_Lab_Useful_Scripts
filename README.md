# Snyder_Lab_Useful_Scripts
Useful scripts for automating common tasks in the lab

### qPCR Analysis

The `qpcr_analysis.py` script will analyze qPCR data using the delta delta Cq method. It takes a csv file as input containing columns corresponding to Sample, Target, and Cq. This sheet can be in the same format as is automatically exported from the thermocycler in the Snyder Lab. It returns an excel file containing new columns corresponding to the calculated delta Cq, delta delta Cq, and relative expression (relative to the input reference sample). 
