# This function will take a csv expression matrix with log2normalized counts from DEseq2 analysis
# as well as a csv files with desired gene sets, and will run ssGSEA analysis for all gene sets
# It will output a new file containing ssGSEA enrichment scores for each sample and gene set

# Load required packages
library(ggplot2)
library(data.table)
library(dplyr)
library(GSVA)

run_ssgsea <- function(input_file, geneset_file) {
  # Read in normalized counts table
  counts = read.csv(input_file)
  rownames(counts) = counts[,1]
  counts = counts[,-1]
  
  # Read in gene set file
  gene_sets = read.csv(geneset_file)
  ssgsea_list = as.list(gene_sets)
  # Remove any NAs or empty strings from ends of lists
  ssgsea_list = lapply(ssgsea_list, function(x) x[x != ""])
  ssgsea_list = lapply(ssgsea_list, function(x) x[!is.na(x)])
  
  # Convert to matrix
  expression_matrix = as.matrix(counts)
  
  # Run ssGSEA on gene expression matrix using input gene sets
  ssgsea_par = ssgseaParam(expression_matrix,ssgsea_list)
  ssgsea_res = gsva(ssgsea_par)
  
  ssgsea_res = as.data.frame(t(ssgsea_res))
  
  write.csv(ssgsea_res, 'ssgsea_results.csv', row.names = T) }

# Example Usage: (Example files can be found in data directory)
#run_ssgsea('example_log2norm_matrix_ssgsea.csv', 'example_gene_sets_ssgsea.csv')
  
  
  
  
  
  