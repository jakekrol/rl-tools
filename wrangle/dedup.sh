#!/usr/bin/env bash

# de duplicate based on key columns

while getopts "i:a:b:o:" opt; do
  case $opt in
    i) input_file="$OPTARG" ;;
    # 1-indexed column nums
    a) col1="$OPTARG" ;;
    b) col2="$OPTARG" ;;
    o) output_file="$OPTARG" ;;
    *) echo "Usage: $0 -i input_file -a col1 -b col2 -o output_file" >&2
       exit 1 ;;
  esac
done

awk -F'\t' -v col1="$col1" -v col2="$col2" \
    '!seen[($col1 <= $col2) ? $col1 FS $col2 : $col2 FS $col1]++' \
    "$input_file" > "$output_file"