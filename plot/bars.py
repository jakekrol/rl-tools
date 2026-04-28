#!/usr/bin/env python3
import sys
import argparse
import matplotlib.pyplot as plt
import plot_helper
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description='Plot a bar graph')

    plot_helper.add_plot_args(parser)

    parser.add_argument("--lw",
                        type=int,
                        default=5,
                        help="line width")

    parser.add_argument("--bar_color",
                        default="black",
                        help="Bar color")
    parser.add_argument("--include-count",
                        action="store_true")

    return parser.parse_args()

def main():
    args = get_args()

    X=[]
    Y=[]
    for l in sys.stdin:
        a = l.rstrip().split()
        if len(a) == 2:
            X.append((a[0]))
            Y.append(float(a[1]))
        else:
            Y.append(int(a[0]))

    if len(X) == 0:
        X = range(len(Y))

    bar_color=args.bar_color

    fig, ax = plt.subplots(figsize=(args.width, args.height))

    if len(bar_color.split(',')) > 1:
        bar_color=bar_color.split(',')
        for i in range(len(X)):
            ax.bar([X[i],
                X[i]],
                [0,Y[i]],
                color=bar_color[i])
            if args.include_count:
                ax.text(X[i], Y[i], str(Y[i]), ha='center', va='bottom')
    else:
        # ax.bar(X, Y, color=bar_color)
        # rotate the x-ticks 
        if args.include_count:
            ax.bar(X, Y, color=bar_color)
            for i in range(len(X)):
                ax.text(X[i], Y[i], str(Y[i]), ha='center', va='bottom')
        else:
            ax.bar(X, Y, color=bar_color, width=0.5)
            ax.set_xticklabels(X, rotation=45, ha='right')


    plot_helper.format_ax(ax, args)
    # rotate x labels again
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(args.output_file, transparent=args.transparent, dpi=300)

if __name__ == '__main__':
    main()
