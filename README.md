# MSCS532 Assignment 2 – Divide-and-Conquer Sorting: Merge Sort vs. Quick Sort

Python implementations of Merge Sort and Quick Sort (Cormen et al., 2022,
Chapters 2 and 7), plus a benchmark that compares them on sorted,
reverse-sorted, and random data.

## Files

| File | Purpose |
|------|---------|
| `sorts.py` | `merge_sort(A)` and `quick_sort(A, randomized=False)` |
| `test_sorts.py` | Unit tests (edge cases, sorted/reverse input, random input) |
| `benchmark.py` | Measures time, peak memory, and key comparisons; writes `results/` |
| `results/results.csv` | Raw benchmark numbers |
| `results/*.png` | Time, comparison-count, and memory charts |

## Algorithms

| Algorithm | Recurrence | Best | Average | Worst | Extra space |
|-----------|------------|------|---------|-------|-------------|
| Merge Sort | T(n) = 2T(n/2) + Θ(n) | Θ(n lg n) | Θ(n lg n) | Θ(n lg n) | Θ(n) |
| Quick Sort (last-element pivot) | T(n) = T(q) + T(n−q−1) + Θ(n) | Θ(n lg n) | Θ(n lg n) | Θ(n²) | O(lg n) stack* |
| Quick Sort (random pivot) | same | Θ(n lg n) | Θ(n lg n) expected | Θ(n²) (very unlikely) | O(lg n) stack* |

\*Quick Sort recurses on the smaller partition and loops on the larger one, so
the stack stays O(lg n) even when the running time is Θ(n²).

## Requirements

Python 3.8+ and `matplotlib` (only needed for the benchmark charts):

```bash
pip install matplotlib
```

## Usage

```bash
python sorts.py            # small demo
python -m unittest -v      # run tests
python benchmark.py        # ~2 minutes; regenerates results/
```

## Key results (n = 10,000; Windows 11, Python 3.13.9)

| Dataset | Merge Sort | Quick Sort (last pivot) | Quick Sort (random pivot) |
|---------|-----------:|------------------------:|--------------------------:|
| Sorted  | 17.8 ms / 69,008 cmp | 4,002.9 ms / 49,995,000 cmp | 13.4 ms / 161,820 cmp |
| Reverse | 18.5 ms / 64,608 cmp | 2,791.0 ms / 49,995,000 cmp | 12.5 ms / 157,306 cmp |
| Random  | 21.4 ms / 120,398 cmp | 11.0 ms / 153,294 cmp | 14.6 ms / 161,634 cmp |

The deterministic Quick Sort makes exactly n(n−1)/2 comparisons on sorted and
reverse-sorted input, its Θ(n²) worst case. Randomizing the pivot removes that
worst case.

## Reference

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
*Introduction to Algorithms* (4th ed.). MIT Press.
