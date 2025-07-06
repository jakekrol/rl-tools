#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Boxplot each column in a table.")
    parser.add_argument('-i', '--input', required=True, help='Input table file (TSV or CSV)')
    parser.add_argument('-o', '--output', required=True, help='Output image file (e.g., plot.png)')
    parser.add_argument('--header', action='store_true', help='Specify if the input file has a header row (default: False)')
    parser.add_argument('--sep', default='\t', help='Column separator (default: tab)')
    parser.add_argument('-t', '--title', type=str, default=None, help='Plot title')
    parser.add_argument('-x', '--xticklabels', type=str, default=None, help='Comma-separated list of x tick labels')
    parser.add_argument('-y', '--ylabel', type=str, default='Values', help='Y-axis label')
    parser.add_argument('-f', '--fontsize', type=int, default=20, help='Font size for labels and title')
    args = parser.parse_args()

    header = 0 if args.header else None
    df = pd.read_csv(args.input, sep=args.sep, header=header)

    plt.figure(figsize=(max(6, len(df.columns)*1.2), 6))
    ax = plt.gca()
    bp = df.boxplot(
        ax=ax,
        patch_artist=True,  # Needed for facecolor
        boxprops=dict(linewidth=2.5, color='black', facecolor='lightgray'),
        whiskerprops=dict(linewidth=2.5, color='black'),
        capprops=dict(linewidth=2.5, color='black'),
        medianprops=dict(linewidth=2.5, color='black'),
        flierprops=dict(markeredgecolor='black', markerfacecolor='none', markersize=6, linewidth=2.5, alpha=0.5),
        return_type='axes'
    )
    plt.grid(alpha=0.15)

    # Set custom x-tick labels if provided
    if args.xticklabels:
        labels = [label.strip() for label in args.xticklabels.split(',')]
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=int(args.fontsize * 0.8))
    else:
        plt.xticks(rotation=45, ha='right', fontsize=int(args.fontsize * 0.8))

    if args.title:
        plt.title(args.title, fontsize=args.fontsize)
    if args.ylabel:
        plt.ylabel(args.ylabel, fontsize=args.fontsize)

    plt.tight_layout()
    plt.savefig(args.output)
    plt.close()

if __name__ == "__main__":
    main()
