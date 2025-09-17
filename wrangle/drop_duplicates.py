#!/usr/bin/env python3

import pandas as pd
import argparse
import os, sys
parser = argparse.ArgumentParser(description='Drop duplicate rows based arguments')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file with potential duplicate rows')
parser.add_argument('-o', '--output', type=str, required=True, help='Output file with duplicates dropped')
parser.add_argument('-c', '--cols', type=str, required=True, help='Comma-separated list of columns to consider for identifying duplicates')
parser.add_argument('--complement', action='store_true', help='If set, use complement of specified columns to identify duplicates')
args = parser.parse_args()

df = pd.read_csv(args.input, sep='\t')
cols = set(args.cols.split(','))
cols = {int(c) for c in cols}
if args.complement:
    all_cols = set(range(1,len(df.columns)+1)) # 1-based indexing
    cols = all_cols - cols
# convert to 0-based indexing
cols = [c-1 for c in cols]
print(f'Dropping duplicates based on columns: {cols}, complement={args.complement}')

# duplicated returns a boolean series, True for duplicates
# all except the first occurrence are marked as True
df = df[~df.iloc[:, cols].duplicated(keep='first')]

df.to_csv(args.output, sep='\t', index=False)
