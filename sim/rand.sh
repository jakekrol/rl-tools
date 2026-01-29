#!/bin/bash

# rand.sh - Fast random line sampling using reservoir sampling
# Usage: cat file.txt | rand.sh n [seed]
#        rand.sh n [seed] < file.txt

usage() {
    echo "Usage: $0 n [seed]"
    echo "  n     - number of random lines to sample"
    echo "  seed  - optional random seed (default: uses current time)"
    echo ""
    echo "Examples:"
    echo "  cat data.txt | $0 1000"
    echo "  $0 500 42 < data.txt"
    echo "  tail -n +2 file.tsv | cut -f 1,2 | $0 100"
    exit 1
}

# Check arguments
if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage
fi

n=$1
seed=${2:-$(date +%s)}

# Validate n is a positive integer
if ! [[ "$n" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: n must be a positive integer" >&2
    exit 1
fi

# Validate seed is an integer
if ! [[ "$seed" =~ ^[0-9]+$ ]]; then
    echo "Error: seed must be a non-negative integer" >&2
    exit 1
fi

# Reservoir sampling with awk
awk -v n="$n" -v seed="$seed" '
BEGIN {
    srand(seed)
}
{
    if (NR <= n) {
        reservoir[NR] = $0
    } else {
        r = int(rand() * NR) + 1
        if (r <= n) {
            reservoir[r] = $0
        }
    }
}
END {
    for (i = 1; i <= (NR < n ? NR : n); i++) {
        if (i in reservoir) {
            print reservoir[i]
        }
    }
}'