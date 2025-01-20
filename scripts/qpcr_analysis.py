#!/Users/gabbyfort/miniconda3/bin/python3

# Import required libraries
import sys
import os 
import argparse
from argparse import RawTextHelpFormatter
import numpy as np
import pandas as pd

# Document and assign input arguments
parser = argparse.ArgumentParser(description=f"This is a script for analyzing qPCR data using the ddcq analysis method.", formatter_class = RawTextHelpFormatter)

parser.add_argument("-f", required = True, help='Input csv file for qpcr analysis. Same format as automatically generated from Snyder Lab Real-Time PCR instrument', dest = 'input_file')

parser.add_argument("-s", required = True, help='Supply name of reference sample.', dest = 'ref_sample')

parser.add_argument("-c", required = False, help='Optional: Input total number of cycles used for qPCR. Default = 40', dest = 'cycles')

parser.add_argument("-g", required = False, help='Optional: Supply reference gene name. Default = Ppia', dest = 'ref_gene')

parser.add_argument("-o", required = False, help='Optional: Supply name of output excel file. Default = qPCR_results', dest = 'output_file')

args = parser.parse_args()


######### Assigning input args to variables ########
input_file = args.input_file
ref_sample = args.ref_sample

if args.ref_gene:
  ref_gene = args.ref_gene
else:
  ref_gene = "PPIA"

if args.cycles:
  cycles = args.cycles
else:
  cycles = 40

if args.output_file:
    output_file = args.output_file
    output_file = f'{output_file}.xlsx'
else:
    output_file = 'qPCR_results.xlsx'


# This function will calculate the average cq value for each set of three technical replicates
def calc_average_cq(input_file, num_cycles):
    input_file = pd.read_csv(input_file)
    input_file = input_file[input_file["Sample"].notna()]
    input_file = input_file.sort_values(by = ['Sample', 'Target'])
    input_file['Cq'] = input_file['Cq'].fillna(float(num_cycles))
    sample_list = list(input_file['Cq'])
    count = 0
    average_list = []
    for sample in sample_list:
        count += 1
        if not count % 3:
            average_list.append(np.mean((sample_list[count-3],sample_list[count-2], sample_list[count-1])))
    average_list = np.repeat(average_list, 3)
    input_file["Average_Cq"] = average_list
    return input_file

# This function will subtract the average cq value for the reference gene from the cq value
# of every other replicate for each sample 
def calc_delta_cq(input_file, ref_gene):
    ref_gene = ref_gene.upper()
    input_file['Target'] = input_file['Target'].str.upper()

    def process_sample(group):
        ref_index = group.index[group['Target'] == ref_gene].tolist()[0]
        refcq = group.loc[ref_index, 'Average_Cq']
        group['delta_cq'] = group['Cq'] - refcq
        return group
    
    result = input_file.groupby("Sample").apply(process_sample)
    result.reset_index(drop=True, inplace=True)
    return result

# This function will canculate the average dcq value for each set of technical replicates
def calc_average_dcq(input_file):
    input_file = input_file.sort_values(by = ['Sample', 'Target'])
    sample_list = list(input_file['delta_cq'])
    count = 0
    average_list = []
    for sample in sample_list:
        count += 1
        if not count % 3:
            average_list.append(np.mean((sample_list[count-3],sample_list[count-2], sample_list[count-1])))
    average_list = np.repeat(average_list, 3)
    input_file["Average_dCq"] = average_list
    return input_file

# This function will subtract the average dcq value for the reference sample
# from each replicate dcq value for every target to obtain ddcq
def calc_ddcq(input_file, ref_sample):
    input_file = input_file.sort_values(by = ['Target'])
    
    def per_target(group, ref_sample):
        group['Sample'] = group['Sample'].apply(lambda x: float(x) if isinstance(x, (int, float)) else str(x).strip().lower())
        ref_sample = float(ref_sample) if ref_sample.replace('.', '', 1).isdigit() else str(ref_sample).strip().lower()
        ref_sample_index = group.index[group['Sample'] == ref_sample].tolist()[0]
        refdcq = group.loc[ref_sample_index, 'Average_dCq']
        group['ddcq'] = group['delta_cq'] - refdcq
        return group
    
    result = input_file.groupby("Target").apply(lambda group: per_target(group, ref_sample))
    result.reset_index(drop=True, inplace=True)
    return result

# This function will calculate relative expression using the following
# equation: 2^(-ddcq)
def calc_relative_exp(input_file):
    relative_exp = 2 ** (-(input_file['ddcq']))
    input_file["relative_expression"] = relative_exp
    input_file = input_file.sort_values(by = ['Target', 'Sample'])
    return input_file

if __name__ == "__main__":
    result = calc_average_cq(input_file,cycles)
    result = calc_delta_cq(result, ref_gene)
    result = calc_average_dcq(result)
    result = calc_ddcq(result, ref_sample)
    result = calc_relative_exp(result)
    result.to_excel(output_file)

