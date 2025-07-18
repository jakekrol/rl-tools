#!/usr/bin/env python3
import sys
import argparse
import matplotlib.pyplot as plt
import plot_helper
import mpltern
import pandas as pd
import itertools

def get_args():
    parser = argparse.ArgumentParser(description='Plot a ternary plot from stdin data.')

    # plot_helper.add_plot_args(parser)
    
    parser.add_argument('-t', '--tlabel', type=str, default='top axis (top)',)
    parser.add_argument('-l', '--llabel', type=str, default='left axis (left)',)
    parser.add_argument('-r', '--rlabel', type=str, default='right axis (right)')
    parser.add_argument('-o', '--output_file', type=str, default='ternary_plot.png',
                        help='Output file name for the plot.')
    parser.add_argument('-n', '--normalize', action='store_true',
                        help='Normalize each row so values sum to 1.')
    parser.add_argument('--tline',default=None, help='line for top axis')
    parser.add_argument('--lline',default=None, help='line for left axis')
    parser.add_argument('--rline',default=None, help='line for right axis')
    return parser.parse_args()

def main():
    args = get_args()

    fig = plt.figure(figsize=(10.8, 4.8))

    # parse data
    x=[]
    y=[]
    z=[]
    c=[]
    for l in sys.stdin:
        a = l.strip().split()
        if len(a) == 3 or len(a) == 4:
            vals = [float(a[0]), float(a[1]), float(a[2])]
            if args.normalize:
                row_sum = sum(vals)
                if row_sum <= 0:
                    raise ValueError(f"Row sum is <= 0, cannot normalize: {a}")
                vals = [v / row_sum for v in vals]
            x.append(vals[0])
            y.append(vals[1])
            z.append(vals[2])
            if len(a) == 4:
                c.append(a[3])
        else:
            raise ValueError(f'Please provide 3 or 4 columns of data, got {len(a)} columns.')
    ### plot
    # handle categories
    if not c:
        c = None
        ax = fig.add_subplot(1,1,1, projection="ternary")
        pc = ax.scatter(x, y, z, s=35, alpha=0.35)
    else:
        # get list of unique categories
        unique_cats = list(dict.fromkeys(c))
        marker_styles = ['o', '^', 's', 'D', 'P', '*', 'X', 'v', '<', '>', 'h', 'H', 'd', 'p', '|', '_', '+', 'x', '1', '2', '3', '4']
        if len(unique_cats) > len(marker_styles):
            raise ValueError(f'Too many categories ({len(unique_cats)}) for the available marker styles ({len(marker_styles)}). Please reduce the number of categories or add more marker styles.')
        marker_cycle = itertools.cycle(marker_styles)
        marker_map = {cat: next(marker_cycle) for cat in unique_cats}
        ax = fig.add_subplot(1,1,1, projection="ternary")
        for cat in unique_cats:
            # get indices of points with this category
            idx = [i for i, val in enumerate(c) if val == cat]
            # scatter points with this category
            ax.scatter([x[i] for i in idx], [y[i] for i in idx], [z[i] for i in idx],
                       marker=marker_map[cat], label=str(cat), s=20, alpha=0.35)
        ax.legend(title="Category", loc='center left', bbox_to_anchor=(1.15, 0.5))
    # labels
    ax.set_tlabel(args.tlabel)
    ax.set_llabel(args.llabel)
    ax.set_rlabel(args.rlabel)
    # limits
    ax.set_ternary_lim(
    -0.05, 1.05,  # tmin, tmax
    -0.05, 1.05,  # lmin, lmax
    -0.05, 1.05,  # rmin, rmax
    )
    # lines
    if args.tline:
        ax.axhline(y=float(args.tline), color='red', linestyle='--', label='Top Line')
    if args.lline:
        ax.axvline(x=float(args.lline), color='blue', linestyle='--', label='Left Line')
    if args.rline:
        ax.axvline(x=float(args.rline), color='green', linestyle='--', label='Right Line')

    plt.tight_layout()
    plt.savefig(args.output_file, dpi=300)
if __name__ == '__main__':
    main()