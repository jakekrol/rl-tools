#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Standard scale a data matrix')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file with data matrix')
parser.add_argument('-o', '--output', type=str, required=True, help='Output file for standardized data matrix')
parser.add_argument('-c', '--columns', type=str, default=None, help='Columns to standardize, comma-separated. If None, all columns are standardized')
parser.add_argument('--header', action='store_true', help='Indicate that the first line of input is a header with column names.')
parser.add_argument('-s', '--stats', type=str, default=None, help='File to save statistics (mean and std) for each column')
args = parser.parse_args()

df = pd.read_csv(args.input, sep='\t', header=0 if args.header else None)
if args.columns:
    cols = args.columns.split(',')
    df = df[cols]
else:
    cols = df.columns.tolist()

# standardize each column
means = {}
stds = {}
for col in cols:
    if df[col].dtype == 'object':
        print(f"Skipping non-numeric column: {col}")
        continue
    mean = df[col].mean()
    std = df[col].std()
    if std == 0:
        print(f"Column {col} has zero standard deviation, skipping standardization.")
        continue
    df[col] = (df[col] - mean) / std
    means[col] = mean
    stds[col] = std

df.to_csv(args.output, sep='\t', header=0 if args.header else None, index=False)

if args.stats:
    stats_df = pd.DataFrame({
        'column': list(means.keys()),
        'mean': list(means.values()),
        'std': list(stds.values())
    })
    stats_df.to_csv(args.stats, sep='\t', index=False)
    print(f"Statistics saved to {args.stats}")

