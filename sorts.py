"""
Divide-and-conquer sorting algorithms: Merge Sort and Quick Sort.

Both follow the procedures in Cormen, Leiserson, Rivest, & Stein,
Introduction to Algorithms (4th ed.), Chapters 2 and 7.
"""

import random


# ---------------------------------------------------------------------------
# Merge Sort  --  T(n) = 2T(n/2) + Theta(n)  =>  Theta(n lg n) in every case
# ---------------------------------------------------------------------------

def merge_sort(A):
    """Return a new list containing the elements of A in increasing order."""
    A = list(A)
    _merge_sort(A, 0, len(A) - 1)
    return A


def _merge_sort(A, p, r):
    """Sort A[p..r] in place (indices are inclusive, as in CLRS)."""
    if p >= r:                      # zero or one element: already sorted
        return
    q = (p + r) // 2                # divide: midpoint
    _merge_sort(A, p, q)            # conquer: sort left half
    _merge_sort(A, q + 1, r)        # conquer: sort right half
    _merge(A, p, q, r)              # combine: merge the two sorted halves


def _merge(A, p, q, r):
    """Merge sorted subarrays A[p..q] and A[q+1..r] into A[p..r]."""
    L = A[p:q + 1]                  # Theta(n) auxiliary space
    R = A[q + 1:r + 1]
    i = j = 0
    k = p
    # Repeatedly copy the smaller front element back into A.
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:            # <= keeps the sort stable
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1
        k += 1
    # Copy whichever side still has elements left.
    while i < len(L):
        A[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        A[k] = R[j]
        j += 1
        k += 1


# ---------------------------------------------------------------------------
# Quick Sort  --  best/average Theta(n lg n), worst case Theta(n^2)
# ---------------------------------------------------------------------------

def quick_sort(A, randomized=False):
    """
    Return a new list containing the elements of A in increasing order.

    randomized=False uses the CLRS last-element pivot (deterministic).
    randomized=True swaps a uniformly random element into the pivot slot
    first (RANDOMIZED-QUICKSORT), giving expected Theta(n lg n) on any input.
    """
    A = list(A)
    _quick_sort(A, 0, len(A) - 1, randomized)
    return A


def _quick_sort(A, p, r, randomized):
    """
    Sort A[p..r] in place.

    To keep the call stack O(lg n) even in the worst case, we recurse on the
    smaller partition and loop on the larger one (tail-call elimination).
    This changes stack depth only; the running time is unchanged.
    """
    while p < r:
        q = _partition(A, p, r, randomized)     # divide; combine is free
        if q - p < r - q:
            _quick_sort(A, p, q - 1, randomized)
            p = q + 1
        else:
            _quick_sort(A, q + 1, r, randomized)
            r = q - 1


def _partition(A, p, r, randomized):
    """Lomuto partition: place pivot at its final index and return it."""
    if randomized:
        s = random.randint(p, r)
        A[s], A[r] = A[r], A[s]
    x = A[r]                        # pivot
    i = p - 1                       # A[p..i] holds elements <= pivot
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1


if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]
    print("Input:            ", data)
    print("Merge sort:       ", merge_sort(data))
    print("Quick sort:       ", quick_sort(data))
    print("Randomized quick: ", quick_sort(data, randomized=True))
