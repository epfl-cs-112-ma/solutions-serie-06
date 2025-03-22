from __future__ import annotations

from typing import Callable

def insert_sorted[T](xs: list[T], y: T, lessThan: Callable[[T, T], bool]) -> list[T]:
    """Inserts an element in a sorted list.

    `xs` must be sorted in increasing order according to the `lessThan`
    comparator.

    Returns a new list `zs` such that `zs` contains `y` and all the elements
    of `xs`, and is sorted.
    """
    zs: list[T] = []
    i = 0

    # First append all the elements of `xs` that are smaller than `y`
    while i < len(xs) and lessThan(xs[i], y):
        zs.append(xs[i])
        i += 1

    # Then append `y`
    zs.append(y)

    # And finally append all the remaining elements of `xs`
    zs.extend(xs[i:]) # xs[i:] is the sublist starting at index i

    return zs

def frequencies[T](xs: list[T]) -> dict[T, int]:
    """Count the number of times each element appears in a list."""
    result: dict[T, int] = {}
    for x in xs:
        result[x] = result.get(x, 0) + 1
    return result
