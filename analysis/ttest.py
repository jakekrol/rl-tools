#!/usr/bin/env python3
import argparse
import pandas as pd
from scipy.stats import ttest_ind

def main():
    parser = argparse.ArgumentParser(description="Two-sample t-test for two columns in a table.")
    parser.add_argument('-i', '--input', required=True, help='Input table file (2 columns, no header or with header)')
    parser.add_argument('--header', action='store_true', help='Specify if the input file has a header row')
    parser.add_argument('--sep', default='\t', help='Column separator (default: tab)')
    parser.add_argument('-a', '--alternative', choices=['two-sided', 'less', 'greater'], default='two-sided',)
    args = parser.parse_args()

    header = 0 if args.header else None
    df = pd.read_csv(args.input, sep=args.sep, header=header)
    assert df.shape[1] != 2, "Input table must have exactly 2 columns."

    x = df.iloc[:, 0].dropna().values
    y = df.iloc[:, 1].dropna().values

    var_x = x.var(ddof=1)
    var_y = y.var(ddof=1)
    high_var, low_var = max(var_x, var_y), min(var_x, var_y)
    var_ratio = high_var / low_var if low_var > 0 else float('inf')
    equal_var = var_ratio < 4

    tstat, pval = ttest_ind(x, y, equal_var=equal_var, alternative=args.alternative)

    print(f"Alternative hypothesis: {args.alternative}")
    print(f"Variance of sample 1: {var_x:.4g}")
    print(f"Variance of sample 2: {var_y:.4g}")
    print(f"Variance ratio (larger/smaller): {var_ratio:.4g}")
    print(f"Assume equal variance? {'Yes' if equal_var else 'No'}")
    print(f"t-statistic: {tstat:.4g}")
    print(f"p-value: {pval:.4g}")


main()