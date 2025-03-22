from algos import *
import pytest

def test_insert_sorted() -> None:
    assert insert_sorted([], 3, lambda a, b: a < b) == [3]
    assert insert_sorted([5, 11, 11, 30], 3, lambda a, b: a < b) == [3, 5, 11, 11, 30]
    assert insert_sorted([5, 11, 11, 30], 7, lambda a, b: a < b) == [5, 7, 11, 11, 30]
    assert insert_sorted([5, 11, 11, 30], 11, lambda a, b: a < b) == [5, 11, 11, 11, 30]
    assert insert_sorted([5, 11, 11, 30], 15, lambda a, b: a < b) == [5, 11, 11, 15, 30]
    assert insert_sorted([5, 11, 11, 30], 33, lambda a, b: a < b) == [5, 11, 11, 30, 33]

    assert insert_sorted([5, 3, 1], 2, lambda a, b: a > b) == [5, 3, 2, 1]

    assert insert_sorted(["bar", "foo"], "aab", lambda a, b: a < b) == ["aab", "bar", "foo"]
    assert insert_sorted(["bar", "foo"], "baz", lambda a, b: a < b) == ["bar", "baz", "foo"]
    assert insert_sorted(["bar", "foo"], "foobar", lambda a, b: a < b) == ["bar", "foo", "foobar"]

def test_frequences() -> None:
    assert frequencies([5, 7, 5, 14, 5, 14]) == {5: 3, 7: 1, 14: 2}
    assert frequencies([]) == dict()
    assert frequencies(["foo", "foo", "bar", "baz"]) == {"foo": 2, "bar": 1, "baz": 1}

    # raises a TypeError if any element is not hashable
    xs = [1]
    with pytest.raises(TypeError):
        frequencies([xs])
