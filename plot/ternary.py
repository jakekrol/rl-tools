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
        if len(a) == 3:
            x.append(float(a[0]))
            y.append(float(a[1]))
            z.append(float(a[2]))
        elif len(a) == 4:
            x.append(float(a[0]))
            y.append(float(a[1]))
            z.append(float(a[2]))
            c.append((a[3]))
        else:
            raise ValueError(f'Please provide 3 or 4 columns of data, got {len(a)} columns.')
    if not c:
        c = None
        ax = fig.add_subplot(1,1,1, projection="ternary")
        pc = ax.scatter(x, y, z)
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
                       marker=marker_map[cat], label=str(cat))
        ax.legend(title="Category", loc='center left', bbox_to_anchor=(1.15, 0.5))
    # scatter
    ax.set_tlabel(args.tlabel)
    ax.set_llabel(args.llabel)
    ax.set_rlabel(args.rlabel)
    plt.tight_layout()
    plt.savefig(args.output_file, dpi=300)
    # plt.savefig(args.output_file, transparent=args.transparent, dpi=300)

if __name__ == '__main__':
    main()