#!/usr/bin/env python3
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


p = argparse.ArgumentParser(
    description="Plot ROC curves and compute AUROC for multiple score files."
)
p.add_argument(
    "-i",
    "--scores",
    required=True,
    help=(
        "Comma-separated list of files. "
        "Each file must have two columns: score,label (no header)."
    ),
)
p.add_argument(
    "-o",
    "--output",
    required=True,
    help="Output image file (e.g. roc.png).",
)
p.add_argument(
    "--title",
    default="ROC curves",
    help="Plot title.",
)
p.add_argument(
    "--names",
    help=(
        "Optional comma-separated list of display names for each scores file. "
        "Must have the same number of entries as --scores if provided."
    ),
)
p.add_argument(
    "--fontsize",
    type=int,
    default=10,
    help="Base font size.",
)
p.add_argument(
    "--figsize",
    type=float,
    nargs=2,
    default=(6, 5),
    metavar=("W", "H"),
    help="Figure size in inches, e.g. --figsize 6 5",
)
p.add_argument(
    "--flip",
    action="store_true",
    help="Flip sign of score (i.e., use -score) before computing ROC.",
)
p.add_argument(
    "--reference"
    , action="store_true",
    help="Plot tpr=fpr line for baseline reference."
)


def load_scores_and_labels(path, score_col=0, label_col=1):
    # Let numpy treat any whitespace as delimiter (works for space/TSV)
    data = np.loadtxt(path, dtype=float)
    if data.ndim == 1:
        raise ValueError(f"File '{path}' must have at least two columns (score, label).")
    y_score = data[:, score_col]
    y_true = data[:, label_col]
    return y_score, y_true


def roc_curve_from_scores(y_true, y_score):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    return fpr, tpr

def auc_from_curve(ytrue, y_score):
    return roc_auc_score(ytrue, y_score)


def main():
    args = p.parse_args()

    plt.figure(figsize=tuple(args.figsize))
    plt.rcParams.update({"font.size": args.fontsize})

    score_paths = [s.strip() for s in args.scores.split(",") if s.strip()]
    if args.names is not None:
        names = [n.strip() for n in args.names.split(",")]
        if len(names) != len(score_paths):
            raise ValueError(
                f"--names has {len(names)} entries but --scores has {len(score_paths)} files."
            )
    else:
        names = None

    curves = []

    for idx, score_path in enumerate(score_paths):
        y_score, y_true = load_scores_and_labels(score_path, score_col=0, label_col=1)
        y_score = np.asarray(y_score, dtype=float)
        y_true = np.asarray(y_true, dtype=float)
        if args.flip:
            y_score = -y_score
        fpr, tpr = roc_curve_from_scores(y_true, y_score)
        auc = auc_from_curve(y_true, y_score)
        label = names[idx] if names is not None else os.path.basename(score_path)
        curves.append((auc, fpr, tpr, label))

    # sort curves by AUC descending so legend appears from best to worst
    curves.sort(key=lambda x: x[0], reverse=True)

    for auc, fpr, tpr, label in curves:
        plt.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})")
    if args.reference:
        plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(args.title)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(args.output, dpi=300)


if __name__ == "__main__":
    main()