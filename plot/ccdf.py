#!/usr/bin/env python3
import sys
import argparse
import matplotlib.pyplot as plt
import plot_helper
from collections import Counter

def get_args():
    parser = argparse.ArgumentParser(description='Plot a line graph')

    plot_helper.add_plot_args(parser)

    parser.add_argument("--delim",
                        default="\t",
                        help="Field delimiter")

    return parser.parse_args()

def main():
    args = get_args()

    fig, ax = plt.subplots(figsize=(args.width, args.height))

    Y=[]
    for l in sys.stdin:
        Y.append(float(l.strip()))
    # compute pdf
    n = len(Y)
    s = sum(Y)
    C = Counter(Y)
    pdf = [(k, v / n) for k, v in C.items()]
    pdf = sorted(pdf,key=lambda x: x[0])
    # cdf
    cdf = []
    c=0
    for x,p in pdf:
        c+=p
        cdf.append((x,c))
    ## ccdf
    ccdf =[]
    ccdf.append((min(Y)-1,1))
    for x,c in cdf:
        ccdf.append((x,1-c))    
    X = [x for x,y in ccdf]
    Y = [y for x,y in ccdf]
    
    h = ax.plot(X,Y)

    plot_helper.format_ax(ax, args)

    plt.tight_layout()
    plt.savefig(args.output_file, transparent=args.transparent, dpi=300)

if __name__ == '__main__':
    main()
