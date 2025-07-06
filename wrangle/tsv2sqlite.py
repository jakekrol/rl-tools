#!/usr/bin/env python3
import argparse
import pandas as pd
import sqlite3

def main():
    parser = argparse.ArgumentParser(description="Convert TSV to SQLite database.")
    parser.add_argument('-i', '--input', required=True, help='Input TSV file')
    parser.add_argument('-o', '--output', required=True, help='Output SQLite file')
    parser.add_argument('-t', '--table', default='data', help='Table name (default: data)')
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep='\t')
    conn = sqlite3.connect(args.output)
    df.to_sql(args.table, conn, index=False, if_exists='replace')
    conn.close()

if __name__ == "__main__":
    main()