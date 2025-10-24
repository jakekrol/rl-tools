#!/usr/bin/env python3
"""
General-purpose file joiner using DuckDB
Performs LEFT JOIN on specified key columns
"""

import argparse
import duckdb
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Join two TSV/CSV files using DuckDB LEFT JOIN"
    )
    
    # File arguments
    parser.add_argument('-l', '--left', required=True, help='Left table file')
    parser.add_argument('-r', '--right', required=True, help='Right table file') 
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    
    # Join key arguments
    parser.add_argument('-k', '--keys', required=True, 
                       help='Comma-separated key columns (e.g., "col1,col2")')
    
    # Optional arguments
    parser.add_argument('--delimiter', default='\t', help='File delimiter (default: tab)')
    parser.add_argument('--no-header', action='store_true', help='Files have no headers')
    
    args = parser.parse_args()
    
    # Parse join keys
    keys = [key.strip() for key in args.keys.split(',')]
    
    # Build JOIN condition
    join_conditions = [f"l.{key} = r.{key}" for key in keys]
    join_clause = " AND ".join(join_conditions)
    
    header = not args.no_header
    
    try:
        con = duckdb.connect()
        
        # Build EXCLUDE clause with double quotes to handle reserved keywords like 'left'
        exclude_clause = ', '.join([f'"{key}"' for key in keys])
        
        query = f"""
        COPY (
            SELECT l.*, r.* EXCLUDE ({exclude_clause})
            FROM read_csv_auto('{args.left}', delim='{args.delimiter}', header={str(header).lower()}) AS l
            LEFT JOIN read_csv_auto('{args.right}', delim='{args.delimiter}', header={str(header).lower()}) AS r
            ON {join_clause}
        ) TO '{args.output}' (FORMAT CSV, DELIMITER '{args.delimiter}', HEADER {str(header).lower()})
        """
        
        print(f"Joining on keys: {', '.join(keys)}")
        con.execute(query)
        print("Join completed!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()