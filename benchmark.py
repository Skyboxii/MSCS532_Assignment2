"""
Benchmark Merge Sort and Quick Sort on sorted, reverse-sorted, and random data.

Records best-of-7 execution time (time.perf_counter) and peak additional memory
(tracemalloc) for each algorithm / dataset / input size, writes the results to
results/results.csv, and saves comparison charts to results/*.png.

Usage:  python benchmark.py
"""

import csv
import os
import random
import time
import tracemalloc

import matplotlib
matplotlib.use("Agg")               # render to files, no window
import matplotlib.pyplot as plt

from sorts import merge_sort, quick_sort

SIZES = [1000, 2500, 5000, 7500, 10000]
REPEATS = 7
SEED = 532
OUT_DIR = "results"

ALGORITHMS = {
    "Merge Sort": merge_sort,
    "Quick Sort (last pivot)": quick_sort,
    "Quick Sort (random pivot)": lambda A: quick_sort(A, randomized=True),
    "Python sorted() (Timsort)": sorted,   # built-in reference point
}

DATASETS = {
    "sorted": lambda n: list(range(n)),
    "reverse": lambda n: list(range(n, 0, -1)),
    "random": lambda n: random.Random(SEED + n).sample(range(n * 10), n),
}


def time_once(sort, data):
    """Wall-clock seconds for one sort of a fresh copy of data."""
    copy = list(data)
    start = time.perf_counter()
    sort(copy)
    return time.perf_counter() - start


def peak_memory(sort, data):
    """Peak bytes allocated while sorting (measured separately from timing,
    because tracemalloc slows Python code down considerably)."""
    copy = list(data)
    tracemalloc.start()
    sort(copy)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


class Counted:
    """Wraps a value and counts every comparison made against it. Comparison
    counts are machine-independent, so they can be checked directly against
    the theoretical bounds (e.g. n(n-1)/2 for Quick Sort's worst case)."""
    count = 0
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __le__(self, other):
        Counted.count += 1
        return self.v <= other.v

    def __lt__(self, other):
        Counted.count += 1
        return self.v < other.v


def comparisons(sort, data):
    """Number of key comparisons made while sorting data."""
    Counted.count = 0
    sort([Counted(x) for x in data])
    return Counted.count


def run():
    random.seed(SEED)                       # makes randomized pivots repeatable
    rows = []
    for dataset, make in DATASETS.items():
        for n in SIZES:
            data = make(n)
            for name, sort in ALGORITHMS.items():
                times = [time_once(sort, data) for _ in range(REPEATS)]
                rows.append({
                    "algorithm": name,
                    "dataset": dataset,
                    "n": n,
                    "time_ms": min(times) * 1000,       # min filters out OS/CPU noise
                    "peak_kb": peak_memory(sort, data) / 1024,
                    "comparisons": comparisons(sort, data),
                })
                print(f"{dataset:8} n={n:6}  {name:27} "
                      f"{rows[-1]['time_ms']:10.2f} ms  {rows[-1]['peak_kb']:9.1f} KB  "
                      f"{rows[-1]['comparisons']:>12,} cmp")
    return rows


def save_csv(rows):
    path = os.path.join(OUT_DIR, "results.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow({k: round(v, 3) if isinstance(v, float) else v
                             for k, v in row.items()})


def plot(rows):
    styles = {
        "Merge Sort": ("#1f77b4", "o"),
        "Quick Sort (last pivot)": ("#d62728", "s"),
        "Quick Sort (random pivot)": ("#2ca02c", "^"),
        "Python sorted() (Timsort)": ("#7f7f7f", "x"),
    }

    # One panel per dataset: metric vs. n (log scale so the Theta(n^2)
    # worst case and the Theta(n lg n) cases fit on one chart).
    metrics = [
        ("time_ms", "Best-of-7 time (ms, log scale)", "time_comparison.png"),
        ("comparisons", "Key comparisons (log scale)", "comparisons_comparison.png"),
    ]
    for metric, ylabel, filename in metrics:
        fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
        for ax, dataset in zip(axes, DATASETS):
            for name, (color, marker) in styles.items():
                pts = [r for r in rows if r["algorithm"] == name and r["dataset"] == dataset]
                ax.plot([p["n"] for p in pts], [p[metric] for p in pts],
                        color=color, marker=marker, label=name)
            ax.set_title(f"{dataset.capitalize()} input")
            ax.set_xlabel("Input size n")
            ax.set_yscale("log")
            ax.grid(True, which="both", alpha=0.3)
        axes[0].set_ylabel(ylabel)
        axes[0].legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(OUT_DIR, filename), dpi=200)
        plt.close(fig)

    # Peak memory at the largest n for each dataset.
    n = SIZES[-1]
    fig, ax = plt.subplots(figsize=(8, 4))
    width = 0.2
    for i, (name, (color, _)) in enumerate(styles.items()):
        vals = [next(r["peak_kb"] for r in rows
                     if r["algorithm"] == name and r["dataset"] == d and r["n"] == n)
                for d in DATASETS]
        ax.bar([x + (i - 1.5) * width for x in range(len(DATASETS))], vals,
               width, color=color, label=name)
    ax.set_xticks(range(len(DATASETS)))
    ax.set_xticklabels([d.capitalize() for d in DATASETS])
    ax.set_ylabel("Peak additional memory (KB)")
    ax.set_title(f"Peak memory while sorting (n = {n:,})")
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "memory_comparison.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = run()
    save_csv(results)
    plot(results)
    print(f"\nSaved results and charts to {OUT_DIR}/")
