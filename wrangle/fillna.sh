#!/usr/bin/env bash

# fill missing

while getopts "i:o:f:" opt; do
  case $opt in
    i) input_file="$OPTARG" ;;
    o) output_file="$OPTARG" ;;
    f) fill_value="$OPTARG" ;;
    *) echo "Usage: $0 -i input_file -o output_file -f fill_value" >&2
       exit 1 ;;
  esac
done
awk \
    -v fill_value="$fill_value" \
    'BEGIN{FS=OFS="\t"} {for(i=1;i<=NF;i++) if($i=="") $i=fill_value; print}' \
    "$input_file" > "$output_file"
