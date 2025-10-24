#!/usr/bin/env bash

# Sort tabular file by column using DuckDB

usage() {
  echo "Usage: $0 -i input -o output -c column [-s ASC|DESC]" >&2
  exit 1
}

input=""
output=""
column=""
order="ASC"

while getopts "i:o:c:s:" opt; do
  case $opt in
    i) input="$OPTARG" ;;
    o) output="$OPTARG" ;;
    c) column="$OPTARG" ;;
    s) order="$OPTARG" ;;
    *) usage ;;
  esac
done

[[ -z "$input" || -z "$output" || -z "$column" ]] && usage

# Sort and write plain TSV
duckdb -c "
COPY (
  SELECT * FROM read_csv('$input', delim='\t', header=true)
  ORDER BY \"$column\" $order
) TO '$output' (HEADER, DELIMITER E'\t');
"

echo "Sorted by '$column' ($order) → $output"