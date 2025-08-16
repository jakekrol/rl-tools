#!/usr/bin/env python3
import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Plot a bipartite network with fixed alignment")
    parser.add_argument("-i", "--input_file", help="Path to the edge list file (CSV/TSV)")
    parser.add_argument("-d", "--delimiter", default="\t", help="File delimiter (default: tab)")
    parser.add_argument("-o", "--output", default="bipartite_plot.png", help="Output image file")
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.input_file, sep=args.delimiter)
    source_col, target_col = df.columns[:2]

    # Create bipartite graph
    G = nx.Graph()
    G.add_edges_from(df[[source_col, target_col]].itertuples(index=False, name=None))

    # Identify node sets
    sources = set(df[source_col])
    targets = set(df[target_col])

    # Sort nodes within each set by descending degree
    source_degrees = {node: G.degree(node) for node in sources}
    target_degrees = {node: G.degree(node) for node in targets}
    sorted_sources = sorted(sources, key=lambda n: source_degrees[n], reverse=True)
    sorted_targets = sorted(targets, key=lambda n: target_degrees[n], reverse=True)

    # Layout: highest degree gets highest y-coordinate (i=0)
    # Correction: highest degree should have lowest y-coordinate (i=0), so reverse the order
    pos = {}
    pos.update((node, (0, len(sorted_sources) - 1 - i)) for i, node in enumerate(sorted_sources))  # left line
    pos.update((node, (1, len(sorted_targets) - 1 - i)) for i, node in enumerate(sorted_targets))  # right line

    # Draw
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color=["skyblue" if n in sources else "lightgreen" for n in G.nodes()])
    plt.title("Bipartite Network", fontsize=14)
    plt.tight_layout()
    plt.savefig(args.output, dpi=300)
    print(f"✅ Saved bipartite plot to {args.output}")

main()
