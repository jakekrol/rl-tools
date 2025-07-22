#!/usr/bin/env python3
import pandas as pd
import os
import sys
import argparse
import time

parser = argparse.ArgumentParser(description='Join two files')
parser.add_argument('-x', '--input1', type=str, required=True, help='Input file 1')
parser.add_argument('-y', '--input2', type=str, required=True, help='Input file 2')
parser.add_argument('-o', '--output', type=str, required=True, help='Output file')
parser.add_argument('-t', '--type', type=str, default='left', help='Join type (inner, outer, left, right)')
parser.add_argument('-k', '--keys', type=str, required=True, help='Join keys (comma separated)')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
parser.add_argument('-i', '--index', action='store_true', help='Tables have index column')
parser.add_argument('-c', '--complement', action='store_true', help='Complement the join, i.e., keep only rows that are not in the other table')
args  = parser.parse_args()

assert os.path.exists(args.input1), f'Input file 1 {args.input1} does not exist'
assert os.path.exists(args.input2), f'Input file 2 {args.input2} does not exist'
args.keys = args.keys.split(',')

print(f'Joining files {args.input1} and {args.input2} on keys {args.keys} with join type {args.type}')
if not args.index:
    df_x = pd.read_csv(args.input1, sep='\t', index_col=None)
    df_y = pd.read_csv(args.input2, sep='\t', index_col=None)
if args.index:
    df_x = pd.read_csv(args.input1, sep='\t', index_col=0)
    df_y = pd.read_csv(args.input2, sep='\t', index_col=0)
if args.verbose:
    print('df_x columns:', df_x.columns.tolist())
    print('df_x:', df_x.head(),sep='\n')
    print('df_y columns:', df_y.columns.tolist())
    print('df_y:', df_y.head(), sep='\n')
if args.complement:
    assert args.type == 'left', 'Complementing the join is only supported for left join'
    print('Complementing the join, i.e., keeping only rows that are in x and not in y')

assert all([key in df_x.columns for key in args.keys]), f'Keys {args.keys} not found in input file 1 {args.input1}'
assert all([key in df_y.columns for key in args.keys]), f'Keys {args.keys} not found in input file 2 {args.input2}'

if args.type == 'left':
    if not args.complement:
        df_merged = pd.merge(df_x, df_y, on=args.keys, how='left')
        df_merged.to_csv(args.output, sep='\t', index=False)
        print(f'Left join completed. Output written to {args.output}')
    else:
        df_merged = pd.merge(df_x, df_y, on=args.keys, how='left', indicator=True)
        df_merged = df_merged[df_merged['_merge'] == 'left_only']
        df_merged.drop(columns=['_merge'], inplace=True)
        # drop columns with suffix _y
        df_merged = df_merged.loc[:, ~df_merged.columns.str.endswith('_y')]
        # rename columns with suffix _x to original names
        df_merged.columns = [col.replace('_x', '') if col.endswith('_x') else col for col in df_merged.columns]
        df_merged.to_csv(args.output, sep='\t', index=False)
        print(f'Left join with complement completed. Output written to {args.output}')
elif args.type == 'outer':
    df_merged = pd.merge(df_x, df_y, on=args.keys, how='outer')
    df_merged.to_csv(args.output, sep='\t', index=False)
    print(f'Outer join completed. Output written to {args.output}')
else: 
    raise ValueError(f'Join type "{args.type}" is not supported. Please use left join.')
