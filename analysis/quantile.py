#!/usr/bin/env python3
import sys
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Compute empirical quantile from a column of values on stdin.")
    parser.add_argument('-q', '--quantile', type=float, required=True, help='Quantile to compute (e.g., 0.75 for 75th percentile)')
    args = parser.parse_args()

    # Read values from stdin, stripping whitespace and ignoring empty lines
    values = [float(line.strip()) for line in sys.stdin if line.strip()]

    if not values:
        print("No values provided on stdin.", file=sys.stderr)
        sys.exit(1)

    quantile_value = np.quantile(values, args.quantile)
    print(quantile_value)

if __name__ == "__main__":
    main()